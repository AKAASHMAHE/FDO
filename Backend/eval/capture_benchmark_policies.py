from __future__ import annotations

import argparse
import csv
import hashlib
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import requests

ROOT = Path(__file__).resolve().parents[2]
DATABASE = ROOT / "Backend" / "fdo_privacy.db"
OUTPUT = ROOT / "Docs" / "eval_results"

try:
    from app.services.policy_discovery_service import (
        MAX_POLICY_BYTES,
        REQUEST_TIMEOUT_SECONDS,
        _html_to_text,
    )
except ModuleNotFoundError:
    import sys

    sys.path.insert(0, str(ROOT / "Backend"))
    from app.services.policy_discovery_service import (
        MAX_POLICY_BYTES,
        REQUEST_TIMEOUT_SECONDS,
        _html_to_text,
    )


SUGGESTED_URLS = {
    "Google Classroom": "https://policies.google.com/privacy",
    "Google Fit": "https://policies.google.com/privacy",
    "Google Home": "https://policies.google.com/privacy",
    "Google Maps": "https://policies.google.com/privacy",
    "Google Pay": "https://policies.google.com/privacy",
    "Google Photos": "https://policies.google.com/privacy",
    "Minecraft": "https://www.minecraft.net/en-us/privacy/gdpr",
    "MyChart": "https://www.epic.com/privacy-policy/",
    "Netflix": "https://help.netflix.com/legal/privacy",
    "PUBG MOBILE": "https://www.pubgmobile.com/privacy.html",
    "PayPal": "https://www.paypal.com/us/legalhub/privacy-full",
    "Reddit": "https://www.reddit.com/policies/privacy-policy",
    "Telegram": "https://telegram.org/privacy",
    "Uber": "https://www.uber.com/legal/en/document/?name=privacy-notice",
    "Uber Eats": "https://www.uber.com/legal/en/document/?name=privacy-notice",
    "WeChat": "https://www.wechat.com/en/privacy_policy.html",
    "WhatsApp": "https://www.whatsapp.com/legal/privacy-policy",
    "YouTube": "https://policies.google.com/privacy",
    "eBay": (
        "https://www.ebay.com/help/policies/member-behavior-policies/"
        "user-privacy-notice-privacy-policy?id=4260"
    ),
}

MANUAL_CAPTURE_CUES = {
    "javascript": (
        "enable javascript",
        "javascript is required",
        "turn on javascript",
        "you need to enable javascript",
    ),
    "cookie gate": (
        "please enable cookies",
        "enable cookies to continue",
        "accept all cookies to continue",
        "accept cookies to continue",
        "cookie consent required",
    ),
    "login gate": (
        "sign in to continue",
        "log in to continue",
        "please sign in",
        "please log in",
        "login required",
        "authenticate to continue",
    ),
}


@dataclass(frozen=True)
class BenchmarkPolicy:
    application_id: str
    application_name: str
    policy_id: str
    source_identifier: str | None


@dataclass(frozen=True)
class PageSnapshot:
    final_url: str
    http_status: int
    fetched_at: str
    cleaned_text: str

    @property
    def text_sha256(self) -> str:
        return hashlib.sha256(self.cleaned_text.encode("utf-8")).hexdigest()


def is_usable_http_url(value: str | None) -> bool:
    if not value or any(character.isspace() for character in value):
        return False
    parsed = urlparse(value)
    return parsed.scheme.lower() in {"http", "https"} and bool(parsed.netloc)


def load_benchmark_policies(database: Path) -> list[BenchmarkPolicy]:
    connection = sqlite3.connect(
        database.resolve().as_uri() + "?mode=ro",
        uri=True,
    )
    connection.row_factory = sqlite3.Row
    try:
        rows = connection.execute(
            """
            SELECT a.application_id, a.application_name,
                   p.policy_id, p.source_identifier
            FROM applications AS a
            JOIN policy_documents AS p
              ON p.application_id = a.application_id
             AND p.policy_id = 'POL-' || a.application_id
            WHERE a.application_id IN (
                SELECT DISTINCT application_id FROM expected_mappings
            )
            ORDER BY a.application_name
            """
        ).fetchall()
    finally:
        connection.close()
    return [
        BenchmarkPolicy(
            application_id=row["application_id"],
            application_name=row["application_name"],
            policy_id=row["policy_id"],
            source_identifier=row["source_identifier"],
        )
        for row in rows
    ]


def fetch_snapshot(url: str) -> PageSnapshot:
    response = requests.get(
        url,
        timeout=REQUEST_TIMEOUT_SECONDS,
        allow_redirects=True,
        headers={"User-Agent": "FDO-Privacy academic policy discovery/1.0"},
    )
    content = response.content[:MAX_POLICY_BYTES]
    encoding = response.encoding or "utf-8"
    html = content.decode(encoding, errors="replace")
    return PageSnapshot(
        final_url=response.url,
        http_status=response.status_code,
        fetched_at=datetime.now(timezone.utc).isoformat(),
        cleaned_text=_html_to_text(html),
    )


def classify_snapshot(snapshot: PageSnapshot) -> tuple[str, str]:
    if not 200 <= snapshot.http_status < 300:
        return "FAILED", f"HTTP {snapshot.http_status}"

    lowered = snapshot.cleaned_text.casefold()
    for cue_group, cues in MANUAL_CAPTURE_CUES.items():
        if any(cue in lowered for cue in cues):
            return "NEEDS_MANUAL_CAPTURE", f"Page requires {cue_group}"

    if len(snapshot.cleaned_text) < 2000:
        return (
            "NEEDS_MANUAL_CAPTURE",
            f"Cleaned text is only {len(snapshot.cleaned_text)} characters "
            "(under 2000; likely shell, gate, or incomplete page)",
        )

    return "CAPTURED", "HTTP response and cleaned text captured"


def ensure_snapshot_table(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS policy_snapshots (
            snapshot_id INTEGER PRIMARY KEY AUTOINCREMENT,
            policy_id TEXT NOT NULL,
            final_url TEXT NOT NULL,
            http_status INTEGER NOT NULL,
            fetched_at TEXT NOT NULL,
            cleaned_text_sha256 TEXT NOT NULL,
            character_count INTEGER NOT NULL,
            cleaned_text TEXT NOT NULL,
            FOREIGN KEY (policy_id) REFERENCES policy_documents(policy_id)
        )
        """
    )


def save_snapshot(connection: sqlite3.Connection, policy_id: str, snapshot: PageSnapshot) -> None:
    connection.execute(
        """
        INSERT INTO policy_snapshots (
            policy_id, final_url, http_status, fetched_at,
            cleaned_text_sha256, character_count, cleaned_text
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            policy_id,
            snapshot.final_url,
            snapshot.http_status,
            snapshot.fetched_at,
            snapshot.text_sha256,
            len(snapshot.cleaned_text),
            snapshot.cleaned_text,
        ),
    )


def output_paths() -> tuple[Path, Path]:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    suffix = 1
    while True:
        extra = "" if suffix == 1 else f"-{suffix}"
        report = OUTPUT / f"policy_capture_report_{stamp}{extra}.csv"
        suggestions = OUTPUT / f"policy_url_suggestions_{stamp}{extra}.csv"
        if not report.exists() and not suggestions.exists():
            return report, suggestions
        suffix += 1


def capture_policies(database: Path = DATABASE) -> tuple[Path, Path]:
    policies = load_benchmark_policies(database)
    if len(policies) != 29:
        raise RuntimeError(
            f"Expected 29 canonical benchmark policies; found {len(policies)}"
        )

    report_path, suggestions_path = output_paths()
    report_rows = []
    suggestions_rows = []
    connection = sqlite3.connect(database)
    try:
        ensure_snapshot_table(connection)
        for policy in policies:
            source_url = policy.source_identifier
            if not is_usable_http_url(source_url):
                suggested_url = SUGGESTED_URLS.get(policy.application_name)
                if not suggested_url:
                    status = "NEEDS_MANUAL_CAPTURE"
                    reason = "Stored source is absent/invalid; no suggestion configured"
                    suggested_url = ""
                else:
                    status = "NEEDS_MANUAL_CAPTURE"
                    reason = "Stored source is absent/invalid; suggestion needs confirmation"
                suggestions_rows.append(
                    {
                        "app": policy.application_name,
                        "policy_id": policy.policy_id,
                        "existing_source_identifier": source_url or "",
                        "suggested_official_policy_url": suggested_url,
                        "needs_human_confirmation": "true",
                    }
                )
                report_rows.append(
                    {
                        "app": policy.application_name,
                        "policy_id": policy.policy_id,
                        "status": status,
                        "reason": reason,
                        "source_identifier": source_url or "",
                        "usable_http_url": "false",
                        "final_url": "",
                        "http_status": "",
                        "character_count": "",
                    }
                )
                continue

            try:
                snapshot = fetch_snapshot(source_url)
            except requests.RequestException as error:
                report_rows.append(
                    {
                        "app": policy.application_name,
                        "policy_id": policy.policy_id,
                        "status": "FAILED",
                        "reason": f"Request failed: {type(error).__name__}: {error}",
                        "source_identifier": source_url,
                        "usable_http_url": "true",
                        "final_url": "",
                        "http_status": "",
                        "character_count": "",
                    }
                )
                continue

            save_snapshot(connection, policy.policy_id, snapshot)
            status, reason = classify_snapshot(snapshot)
            report_rows.append(
                {
                    "app": policy.application_name,
                    "policy_id": policy.policy_id,
                    "status": status,
                    "reason": reason,
                    "source_identifier": source_url,
                    "usable_http_url": "true",
                    "final_url": snapshot.final_url,
                    "http_status": snapshot.http_status,
                    "character_count": len(snapshot.cleaned_text),
                }
            )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

    with report_path.open("x", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(report_rows[0]))
        writer.writeheader()
        writer.writerows(report_rows)
    with suggestions_path.open("x", newline="", encoding="utf-8") as file:
        fieldnames = [
            "app",
            "policy_id",
            "existing_source_identifier",
            "suggested_official_policy_url",
            "needs_human_confirmation",
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(suggestions_rows)
    return report_path, suggestions_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Capture live policy snapshots for the 29 canonical benchmark policies."
    )
    parser.add_argument("--database", type=Path, default=DATABASE)
    arguments = parser.parse_args()
    report, suggestions = capture_policies(arguments.database)
    print(f"Capture report: {report}")
    print(f"URL suggestions (not fetched): {suggestions}")


if __name__ == "__main__":
    main()
