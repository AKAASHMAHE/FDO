from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import shutil
import sqlite3
import sys
import time
import uuid
from collections import Counter
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "Backend"
EVAL = BACKEND / "eval"
OUTPUT = ROOT / "Docs" / "eval_results"
FROZEN_DATABASE = EVAL / "frozen_policy_capture_20261014T112903+0530.sqlite"
WORKING_DATABASE = EVAL / "policy_extraction_working_20261014T112903+0530.sqlite"
INITIAL_CAPTURE_REPORT = (
    OUTPUT / "policy_capture_report_20261014T053908Z.csv"
)

if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from app.services import policy_extraction_service
from app.services.ai_service import MODEL_NAME, _load_env_file
from app.services.comparison_service import classify_purposes
from app.services.policy_discovery_service import _html_to_text
from app.services.policy_extraction_service import extract_policy_evidence

CHUNK_TARGET_CHARS = 10_000
CHUNK_OVERLAP_CHARS = 1_000
RETRY_DELAYS_SECONDS = (1, 2)
ACCEPTED_CAPTURE_STATUSES = {"CAPTURED", "MANUALLY_CAPTURED"}
RENDERED_PAGE_NOTES = {
    "POL-EDU-02": (
        "Manual capture required: direct capture was 8 characters; user reports "
        "rendered body 30,715 characters, but headless Playwright is unavailable "
        "and rendered text was not supplied as an import file."
    ),
    "POL-SOC-01": (
        "Manual capture required: direct Instagram host yielded 58 characters; "
        "Meta Privacy Policy may cover Instagram, but its applicability/text "
        "was not verified for import."
    ),
    "POL-HEA-02": (
        "Manual capture required: direct capture was 972 characters; user reports "
        "rendered body 53,584 characters, but headless Playwright is unavailable "
        "and rendered text was not supplied as an import file."
    ),
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _ensure_working_database() -> Path:
    if not WORKING_DATABASE.exists():
        if not FROZEN_DATABASE.exists():
            raise FileNotFoundError(f"Frozen database not found: {FROZEN_DATABASE}")
        shutil.copy2(FROZEN_DATABASE, WORKING_DATABASE)
    return WORKING_DATABASE


def _connect(database: Path, *, read_only: bool = False) -> sqlite3.Connection:
    if read_only:
        connection = sqlite3.connect(
            database.resolve().as_uri() + "?mode=ro",
            uri=True,
        )
    else:
        connection = sqlite3.connect(database)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def _capture_report_statuses(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    with path.open(encoding="utf-8", newline="") as file:
        return {
            row["policy_id"]: row["status"]
            for row in csv.DictReader(file)
            if row.get("policy_id") and row.get("status")
        }


def ensure_extraction_schema(
    connection: sqlite3.Connection,
    capture_statuses: dict[str, str] | None = None,
) -> None:
    columns = {
        row["name"]
        for row in connection.execute("PRAGMA table_info(policy_snapshots)")
    }
    if not columns:
        raise RuntimeError("policy_snapshots table is missing")
    additions = {
        "scope": "TEXT NOT NULL DEFAULT 'full_policy'",
        "source_note": "TEXT NOT NULL DEFAULT 'Legacy snapshot; source note unavailable'",
        "capture_status": "TEXT NOT NULL DEFAULT 'NEEDS_MANUAL_CAPTURE'",
        "capture_method": "TEXT NOT NULL DEFAULT 'LIVE'",
    }
    for name, declaration in additions.items():
        if name not in columns:
            connection.execute(
                f"ALTER TABLE policy_snapshots ADD COLUMN {name} {declaration}"
            )

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS extraction_runs (
            run_id TEXT PRIMARY KEY,
            snapshot_id INTEGER NOT NULL,
            policy_id TEXT NOT NULL,
            scope TEXT NOT NULL,
            started_at TEXT NOT NULL,
            completed_at TEXT,
            model_name TEXT NOT NULL,
            extraction_method TEXT NOT NULL,
            run_status TEXT NOT NULL,
            chunk_count INTEGER NOT NULL DEFAULT 0,
            extracted_row_count INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (snapshot_id) REFERENCES policy_snapshots(snapshot_id),
            FOREIGN KEY (policy_id) REFERENCES policy_documents(policy_id)
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS extracted_evidence (
            extracted_evidence_id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id TEXT NOT NULL,
            policy_id TEXT NOT NULL,
            snapshot_id INTEGER NOT NULL,
            chunk_index INTEGER NOT NULL,
            data_type TEXT,
            purpose TEXT,
            entity TEXT,
            sharing TEXT,
            retention TEXT,
            evidence_text TEXT NOT NULL,
            source_section TEXT,
            extraction_status TEXT NOT NULL,
            confidence REAL,
            model_name TEXT NOT NULL,
            extraction_method TEXT NOT NULL,
            dedupe_key TEXT NOT NULL,
            UNIQUE (run_id, dedupe_key),
            FOREIGN KEY (run_id) REFERENCES extraction_runs(run_id),
            FOREIGN KEY (policy_id) REFERENCES policy_documents(policy_id),
            FOREIGN KEY (snapshot_id) REFERENCES policy_snapshots(snapshot_id)
        )
        """
    )

    for policy_id, status in (capture_statuses or {}).items():
        if status not in {
            "CAPTURED",
            "NEEDS_MANUAL_CAPTURE",
            "FAILED",
        }:
            continue
        connection.execute(
            """
            UPDATE policy_snapshots
            SET capture_status = ?,
                scope = CASE
                    WHEN scope = 'full_policy' THEN 'full_policy'
                    ELSE scope
                END,
                source_note = CASE
                    WHEN source_note = 'Legacy snapshot; source note unavailable'
                    THEN 'Live capture from stored policy source; initial evaluation run'
                    ELSE source_note
                END
            WHERE policy_id = ?
              AND capture_method = 'LIVE'
              AND capture_status = 'NEEDS_MANUAL_CAPTURE'
            """,
            (status, policy_id),
        )


def _validate_utc_timestamp(value: str) -> str:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError("fetched_at must be an ISO-8601 UTC timestamp") from error
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("fetched_at must include an explicit UTC timezone")
    if parsed.utcoffset().total_seconds() != 0:
        raise ValueError("fetched_at must be in UTC")
    return parsed.astimezone(timezone.utc).isoformat()


def import_manual_snapshot(
    database: Path,
    *,
    file_path: Path,
    policy_id: str,
    final_url: str,
    http_status: int,
    fetched_at: str,
    scope: str,
    source_note: str,
    is_html: bool = False,
) -> int:
    if not policy_id.strip():
        raise ValueError("policy_id is required")
    parsed_url = urlparse(final_url)
    if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
        raise ValueError("final_url must be a valid http(s) URL")
    if not 200 <= http_status < 300:
        raise ValueError("manual snapshot HTTP status must be 2xx")
    if not scope.strip() or not source_note.strip():
        raise ValueError("scope and source_note are required")
    timestamp = _validate_utc_timestamp(fetched_at)
    content = file_path.read_text(encoding="utf-8")
    cleaned_text = _html_to_text(content) if is_html else "\n".join(
        line.strip() for line in content.splitlines() if line.strip()
    )
    if not cleaned_text:
        raise ValueError("manual snapshot file contains no text")

    connection = _connect(database)
    try:
        ensure_extraction_schema(connection, _capture_report_statuses(INITIAL_CAPTURE_REPORT))
        known = connection.execute(
            "SELECT 1 FROM policy_documents WHERE policy_id = ?",
            (policy_id,),
        ).fetchone()
        if not known:
            raise ValueError(f"Unknown policy_id: {policy_id}")
        cursor = connection.execute(
            """
            INSERT INTO policy_snapshots (
                policy_id, final_url, http_status, fetched_at,
                cleaned_text_sha256, character_count, cleaned_text,
                scope, source_note, capture_status, capture_method
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'MANUALLY_CAPTURED', 'MANUAL')
            """,
            (
                policy_id,
                final_url,
                http_status,
                timestamp,
                hashlib.sha256(cleaned_text.encode("utf-8")).hexdigest(),
                len(cleaned_text),
                cleaned_text,
                scope.strip(),
                source_note.strip(),
            ),
        )
        connection.commit()
        return int(cursor.lastrowid)
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def _is_heading(line: str) -> bool:
    text = line.strip()
    return (
        2 <= len(text) <= 120
        and not re.search(r"[.!?]$", text)
        and (
            text.isupper()
            or bool(re.match(r"^(section\s+)?\d+([.)]\d+)*[.):]?\s+\S", text, re.I))
            or (len(text.split()) <= 12 and text.istitle())
        )
    )


def _split_long_block(block: str) -> list[str]:
    pieces: list[str] = []
    remaining = block.strip()
    while len(remaining) > CHUNK_TARGET_CHARS:
        boundary = remaining.rfind("\n", 0, CHUNK_TARGET_CHARS)
        if boundary < CHUNK_TARGET_CHARS // 2:
            boundary = remaining.rfind(". ", 0, CHUNK_TARGET_CHARS)
        if boundary < CHUNK_TARGET_CHARS // 2:
            boundary = CHUNK_TARGET_CHARS
        else:
            boundary += 1
        pieces.append(remaining[:boundary].strip())
        carry_from = max(0, boundary - CHUNK_OVERLAP_CHARS)
        remaining = remaining[carry_from:].strip()
        if len(remaining) > 0 and len(remaining) >= len(block):
            raise RuntimeError("Chunking made no progress")
    if remaining:
        pieces.append(remaining)
    return pieces


def chunk_policy_text(
    text: str,
    target_chars: int = CHUNK_TARGET_CHARS,
    overlap_chars: int = CHUNK_OVERLAP_CHARS,
) -> list[str]:
    if target_chars != CHUNK_TARGET_CHARS or overlap_chars != CHUNK_OVERLAP_CHARS:
        raise ValueError("The evaluation chunker uses 10000-char chunks and 1000-char overlap")
    sections: list[str] = []
    current: list[str] = []
    for line in text.splitlines():
        if _is_heading(line) and current:
            sections.append("\n".join(current).strip())
            current = [line]
        else:
            current.append(line)
    if current:
        sections.append("\n".join(current).strip())

    chunks: list[str] = []
    active = ""
    for section in sections:
        if not section:
            continue
        if len(section) > CHUNK_TARGET_CHARS:
            if active:
                chunks.append(active)
                active = ""
            chunks.extend(_split_long_block(section))
            continue
        candidate = f"{active}\n\n{section}".strip() if active else section
        if len(candidate) <= CHUNK_TARGET_CHARS:
            active = candidate
            continue
        if active:
            chunks.append(active)
        carry = active[-CHUNK_OVERLAP_CHARS:] if active else ""
        active = f"{carry}\n\n{section}".strip()
        if len(active) > CHUNK_TARGET_CHARS:
            chunks.extend(_split_long_block(active))
            active = ""
    if active:
        chunks.append(active)
    return chunks


def _retryable_llm_error(error: Exception) -> bool:
    values = [
        getattr(error, "status_code", None),
        getattr(error, "code", None),
        getattr(getattr(error, "response", None), "status_code", None),
    ]
    for value in values:
        try:
            status = int(value)
        except (TypeError, ValueError):
            continue
        if status == 429 or status >= 500:
            return True
    message = str(error).lower()
    return any(token in message for token in ("429", "rate limit", "503", "502", "500", "504"))


@contextmanager
def _force_existing_regex_fallback():
    original = policy_extraction_service.extract_policy_evidence_with_ai

    def fail_ai(*_args, **_kwargs):
        raise RuntimeError("LLM unavailable; use existing regex fallback")

    policy_extraction_service.extract_policy_evidence_with_ai = fail_ai
    try:
        yield
    finally:
        policy_extraction_service.extract_policy_evidence_with_ai = original


def _extract_chunk(text: str, application_name: str) -> tuple[list[dict], str]:
    _load_env_file()
    if not os.getenv("GEMINI_API_KEY"):
        return (
            extract_policy_evidence(text, application_name),
            "REGEX_FALLBACK",
        )

    from app.services.ai_service import extract_policy_evidence_with_ai

    for attempt in range(len(RETRY_DELAYS_SECONDS) + 1):
        try:
            return (
                extract_policy_evidence_with_ai(text, application_name),
                "LLM",
            )
        except Exception as error:
            if not _retryable_llm_error(error):
                break
            if attempt < len(RETRY_DELAYS_SECONDS):
                time.sleep(RETRY_DELAYS_SECONDS[attempt])
    with _force_existing_regex_fallback():
        return (
            extract_policy_evidence(text, application_name),
            "REGEX_FALLBACK",
        )


def _dedupe_key(item: dict) -> str:
    fields = (
        item.get("data_type"),
        item.get("purpose"),
        item.get("entity"),
        item.get("sharing"),
        item.get("retention"),
        " ".join(str(item.get("evidence_text") or "").split()).casefold(),
    )
    return hashlib.sha256(
        json.dumps(fields, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _get_benchmark_policies(
    connection: sqlite3.Connection,
    benchmark_policy_ids: list[str],
) -> list[sqlite3.Row]:
    if not benchmark_policy_ids:
        return []
    placeholders = ",".join("?" for _ in benchmark_policy_ids)
    return connection.execute(
        f"""
        SELECT p.policy_id, p.application_id, a.application_name
        FROM policy_documents AS p
        JOIN applications AS a ON a.application_id = p.application_id
        WHERE p.policy_id = 'POL-' || p.application_id
          AND p.policy_id IN ({placeholders})
        ORDER BY a.application_name
        """,
        benchmark_policy_ids,
    ).fetchall()


def _latest_snapshots(connection: sqlite3.Connection) -> dict[str, sqlite3.Row]:
    rows = connection.execute(
        """
        SELECT snapshot_id, policy_id, final_url, http_status, fetched_at,
               cleaned_text_sha256, character_count, cleaned_text, scope,
               source_note, capture_status, capture_method
        FROM policy_snapshots
        ORDER BY snapshot_id
        """
    ).fetchall()
    latest = {}
    for row in rows:
        latest[row["policy_id"]] = row
    return latest


def _purpose_summary(items: list[sqlite3.Row]) -> tuple[dict[str, int], int]:
    categories: Counter[str] = Counter()
    unclassified = 0
    for item in items:
        found = classify_purposes(item["purpose"] or "")
        if found:
            categories.update(found)
        else:
            unclassified += 1
    return dict(sorted(categories.items())), unclassified


def _timestamped_report_path() -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    suffix = 1
    while True:
        extra = "" if suffix == 1 else f"-{suffix}"
        path = OUTPUT / f"policy_snapshot_extraction_report_{stamp}{extra}.csv"
        if not path.exists():
            return path
        suffix += 1


def run_extraction(database: Path) -> Path:
    capture_statuses = _capture_report_statuses(INITIAL_CAPTURE_REPORT)
    connection = _connect(database)
    report_path = _timestamped_report_path()
    try:
        ensure_extraction_schema(connection, capture_statuses)
        connection.commit()
        policies = _get_benchmark_policies(
            connection,
            sorted(capture_statuses),
        )
        latest = _latest_snapshots(connection)
        hash_groups: dict[str, list[str]] = {}
        for policy_id, snapshot in latest.items():
            if snapshot["capture_status"] in ACCEPTED_CAPTURE_STATUSES:
                hash_groups.setdefault(snapshot["cleaned_text_sha256"], []).append(policy_id)

        output_rows = []
        for policy in policies:
            policy_id = policy["policy_id"]
            snapshot = latest.get(policy_id)
            if snapshot is None:
                policy_status = capture_statuses.get(policy_id, "NO_SNAPSHOT")
                reason = (
                    "No stored snapshot; invalid/absent source needs manual capture. "
                    "The suggested URL, if any, was not fetched."
                    if policy_status == "NEEDS_MANUAL_CAPTURE"
                    else "No snapshot record"
                )
                output_rows.append(
                    _empty_report_row(policy, policy_status, reason)
                )
                continue
            if snapshot["capture_status"] not in ACCEPTED_CAPTURE_STATUSES:
                output_rows.append(
                    _empty_report_row(
                        policy,
                        snapshot["capture_status"],
                        "Snapshot excluded: capture is not marked CAPTURED or MANUALLY_CAPTURED",
                        snapshot,
                    )
                )
                continue

            chunks = chunk_policy_text(snapshot["cleaned_text"])
            if not chunks:
                output_rows.append(
                    _empty_report_row(policy, "FAILED", "Snapshot text is empty", snapshot)
                )
                continue

            previous = connection.execute(
                """
                SELECT run_id, model_name, extraction_method, chunk_count
                FROM extraction_runs
                WHERE snapshot_id = ? AND run_status = 'COMPLETED'
                ORDER BY completed_at DESC
                LIMIT 1
                """,
                (snapshot["snapshot_id"],),
            ).fetchone()
            if previous:
                prior_evidence = connection.execute(
                    """
                    SELECT data_type, purpose, extraction_method
                    FROM extracted_evidence
                    WHERE run_id = ?
                    """,
                    (previous["run_id"],),
                ).fetchall()
                purpose_counts, unclassified = _purpose_summary(prior_evidence)
                same_hash = hash_groups.get(snapshot["cleaned_text_sha256"], [])
                output_rows.append(
                    {
                        "app": policy["application_name"],
                        "policy_id": policy_id,
                        "snapshot_status": snapshot["capture_status"],
                        "capture_method": snapshot["capture_method"],
                        "scope": snapshot["scope"],
                        "character_count": snapshot["character_count"],
                        "chunk_count": previous["chunk_count"],
                        "extracted_rows": len(prior_evidence),
                        "distinct_data_types": json.dumps(
                            sorted({
                                row["data_type"]
                                for row in prior_evidence
                                if row["data_type"]
                            }),
                            ensure_ascii=False,
                        ),
                        "counts_by_purpose_category": json.dumps(
                            purpose_counts,
                            ensure_ascii=False,
                            sort_keys=True,
                        ),
                        "unclassified_purpose_rows": unclassified,
                        "data_other_rows": sum(
                            row["data_type"] == "DATA.OTHER"
                            for row in prior_evidence
                        ),
                        "umbrella_same_hash_policy_count": len(same_hash),
                        "umbrella_same_hash_policy_ids": ";".join(
                            sorted(same_hash)
                        ),
                        "extraction_model": previous["model_name"],
                        "extraction_method": previous["extraction_method"],
                        "run_id": previous["run_id"],
                        "reason": "",
                    }
                )
                continue

            run_id = str(uuid.uuid4())
            started_at = utc_now()
            connection.execute(
                """
                INSERT INTO extraction_runs (
                    run_id, snapshot_id, policy_id, scope, started_at,
                    model_name, extraction_method, run_status, chunk_count
                ) VALUES (?, ?, ?, ?, ?, ?, 'PENDING', 'RUNNING', ?)
                """,
                (
                    run_id,
                    snapshot["snapshot_id"],
                    policy_id,
                    snapshot["scope"],
                    started_at,
                    MODEL_NAME,
                    len(chunks),
                ),
            )

            dedupe_seen: set[str] = set()
            run_methods: set[str] = set()
            for chunk_index, chunk in enumerate(chunks, start=1):
                evidence, method = _extract_chunk(
                    chunk,
                    policy["application_name"],
                )
                run_methods.add(method)
                for item in evidence:
                    evidence_text = str(item.get("evidence_text") or "").strip()
                    if not evidence_text:
                        continue
                    if not item.get("source_section"):
                        item["source_section"] = None
                    key = _dedupe_key(item)
                    if key in dedupe_seen:
                        continue
                    dedupe_seen.add(key)
                    connection.execute(
                        """
                        INSERT OR IGNORE INTO extracted_evidence (
                            run_id, policy_id, snapshot_id, chunk_index,
                            data_type, purpose, entity, sharing, retention,
                            evidence_text, source_section, extraction_status,
                            confidence, model_name, extraction_method, dedupe_key
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            run_id,
                            policy_id,
                            snapshot["snapshot_id"],
                            chunk_index,
                            item.get("data_type"),
                            item.get("purpose"),
                            item.get("entity"),
                            item.get("sharing"),
                            item.get("retention"),
                            evidence_text,
                            item.get("source_section"),
                            item.get("extraction_status") or "EXTRACTED",
                            item.get("confidence"),
                            MODEL_NAME,
                            method,
                            key,
                        ),
                    )

            methods = sorted(run_methods)
            method_name = methods[0] if len(methods) == 1 else "MIXED"
            connection.execute(
                """
                UPDATE extraction_runs
                SET completed_at = ?, extraction_method = ?,
                    run_status = 'COMPLETED',
                    extracted_row_count = (
                        SELECT COUNT(*) FROM extracted_evidence WHERE run_id = ?
                    )
                WHERE run_id = ?
                """,
                (utc_now(), method_name, run_id, run_id),
            )
            stored_rows = connection.execute(
                """
                SELECT data_type, purpose, extraction_method
                FROM extracted_evidence
                WHERE run_id = ?
                """,
                (run_id,),
            ).fetchall()
            purpose_counts, unclassified = _purpose_summary(stored_rows)
            same_hash = hash_groups.get(snapshot["cleaned_text_sha256"], [])
            output_rows.append(
                {
                    "app": policy["application_name"],
                    "policy_id": policy_id,
                    "snapshot_status": snapshot["capture_status"],
                    "capture_method": snapshot["capture_method"],
                    "scope": snapshot["scope"],
                    "character_count": snapshot["character_count"],
                    "chunk_count": len(chunks),
                    "extracted_rows": len(stored_rows),
                    "distinct_data_types": json.dumps(
                        sorted({row["data_type"] for row in stored_rows if row["data_type"]}),
                        ensure_ascii=False,
                    ),
                    "counts_by_purpose_category": json.dumps(
                        purpose_counts,
                        ensure_ascii=False,
                        sort_keys=True,
                    ),
                    "unclassified_purpose_rows": unclassified,
                    "data_other_rows": sum(
                        row["data_type"] == "DATA.OTHER" for row in stored_rows
                    ),
                    "umbrella_same_hash_policy_count": len(same_hash),
                    "umbrella_same_hash_policy_ids": ";".join(sorted(same_hash)),
                    "extraction_model": MODEL_NAME,
                    "extraction_method": method_name,
                    "run_id": run_id,
                    "reason": "",
                }
            )

        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

    fields = [
        "app",
        "policy_id",
        "snapshot_status",
        "capture_method",
        "scope",
        "character_count",
        "chunk_count",
        "extracted_rows",
        "distinct_data_types",
        "counts_by_purpose_category",
        "unclassified_purpose_rows",
        "data_other_rows",
        "umbrella_same_hash_policy_count",
        "umbrella_same_hash_policy_ids",
        "extraction_model",
        "extraction_method",
        "run_id",
        "reason",
    ]
    with report_path.open("x", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(output_rows)
    return report_path


def _empty_report_row(
    policy: sqlite3.Row,
    status: str,
    reason: str,
    snapshot: sqlite3.Row | None = None,
) -> dict:
    reason = RENDERED_PAGE_NOTES.get(policy["policy_id"], reason)
    return {
        "app": policy["application_name"],
        "policy_id": policy["policy_id"],
        "snapshot_status": status,
        "capture_method": snapshot["capture_method"] if snapshot else "",
        "scope": snapshot["scope"] if snapshot else "not captured",
        "character_count": snapshot["character_count"] if snapshot else 0,
        "chunk_count": 0,
        "extracted_rows": 0,
        "distinct_data_types": "[]",
        "counts_by_purpose_category": "{}",
        "unclassified_purpose_rows": 0,
        "data_other_rows": 0,
        "umbrella_same_hash_policy_count": 0,
        "umbrella_same_hash_policy_ids": "",
        "extraction_model": MODEL_NAME,
        "extraction_method": "NONE",
        "run_id": "",
        "reason": reason,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Import manual policy captures or extract from eligible snapshots."
    )
    parser.add_argument("--database", type=Path, default=None)
    parser.add_argument("--from-file", type=Path)
    parser.add_argument("--policy-id")
    parser.add_argument("--final-url")
    parser.add_argument("--http-status", type=int)
    parser.add_argument("--fetched-at")
    parser.add_argument("--scope")
    parser.add_argument("--source-note")
    parser.add_argument("--html", action="store_true")
    arguments = parser.parse_args()

    if arguments.from_file:
        database = arguments.database or _ensure_working_database()
        required = (
            arguments.policy_id,
            arguments.final_url,
            arguments.http_status,
            arguments.fetched_at,
            arguments.scope,
            arguments.source_note,
        )
        if any(value is None for value in required):
            parser.error(
                "--from-file requires --policy-id, --final-url, --http-status, "
                "--fetched-at (UTC), --scope, and --source-note"
            )
        snapshot_id = import_manual_snapshot(
            database,
            file_path=arguments.from_file,
            policy_id=arguments.policy_id,
            final_url=arguments.final_url,
            http_status=arguments.http_status,
            fetched_at=arguments.fetched_at,
            scope=arguments.scope,
            source_note=arguments.source_note,
            is_html=arguments.html,
        )
        print(f"Imported MANUALLY_CAPTURED snapshot_id={snapshot_id} into {database}")
        return

    database = arguments.database or _ensure_working_database()
    report = run_extraction(database)
    print(f"Extraction report: {report}")
    print(f"Extraction database: {database}")


if __name__ == "__main__":
    main()
