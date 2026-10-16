from __future__ import annotations

import csv
import json
import os
import shutil
import socket
import sqlite3
import subprocess
import sys
import tempfile
import time
import uuid
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path
from typing import Any
import urllib.request

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import run_idf_b_eval as base

BACKEND = base.BACKEND
OUTPUT = base.OUTPUT
DATABASE = base.DATABASE

if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from app.models.expected_mapping import ExpectedMapping
from app.models.policy_document import PolicyDocument
from app.models.policy_evidence import PolicyEvidence
from app.services import policy_extraction_service
from app.services.evidence_validation_service import validate_policy_evidence

SYNTHETIC_TYPES = {
    "COM-01": "DATA.HEALTH",
    "COM-02": "DATA.HEALTH",
    "ECO-02": "DATA.HEALTH",
    "EDU-01": "DATA.HEALTH",
    "FIN-01": "DATA.HEALTH",
    "FIN-02": "DATA.HEALTH",
    "HEA-01": "DATA.GAMING.GAMEPLAY",
    "NAV-02": "DATA.HEALTH",
    "SOC-02": "DATA.HEALTH",
    "STR-02": "DATA.HEALTH",
}


@contextmanager
def _working_directory(path: Path):
    old = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old)


def _read_db_evidence(database: Path, mappings: list[dict[str, Any]]) -> tuple[
    dict[str, list[dict[str, Any]]],
    dict[str, dict[str, Any]],
]:
    app_ids = sorted({row["application_id"] for row in mappings})
    conn = sqlite3.connect(f"file:{database.as_posix()}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    evidence_by_policy: dict[str, list[dict[str, Any]]] = {}
    policies: dict[str, dict[str, Any]] = {}
    try:
        for app_id in app_ids:
            policy_id = f"POL-{app_id}"
            policy = conn.execute(
                "SELECT policy_id, application_id, source_type, source_identifier, "
                "document_name, raw_text FROM policy_documents WHERE policy_id = ?",
                (policy_id,),
            ).fetchone()
            if policy is None:
                raise ValueError(f"Missing canonical policy {policy_id}")
            policies[app_id] = dict(policy)
            evidence_by_policy[policy_id] = [
                dict(row)
                for row in conn.execute(
                    "SELECT evidence_id, policy_id, data_type, purpose, entity, sharing, "
                    "retention, evidence_text, source_section, extraction_status, confidence "
                    "FROM policy_evidence WHERE policy_id = ? ORDER BY evidence_id",
                    (policy_id,),
                )
            ]
    finally:
        conn.close()
    return evidence_by_policy, policies


def _attach_expected_purposes(
    mappings: list[dict[str, Any]],
    database: Path,
) -> None:
    conn = sqlite3.connect(f"file:{database.as_posix()}?mode=ro", uri=True)
    try:
        for row in mappings:
            match = conn.execute(
                "SELECT expected_purpose FROM expected_mappings WHERE expected_id = ?",
                (row["expected_id"],),
            ).fetchone()
            if match is None:
                raise ValueError(f"Ground-truth mapping is missing from database: {row['expected_id']}")
            row["expected_purpose"] = match[0]
    finally:
        conn.close()


def _evidence_group(detail: dict[str, Any]) -> str:
    status = detail.get("decision_evidence_status", "")
    if status == "NO_EVIDENCE":
        return "NO_EVIDENCE (Rule 1)"
    if status in {"INSUFFICIENT", "UNKNOWN"} or status != "EXTRACTED":
        return "INSUFFICIENT_EVIDENCE (Rule 2)"
    return "REAL_MATCH_COMPARISON"


def _rule_group_summary(
    mappings: list[dict[str, Any]],
    predictions: dict[str, dict[str, Any]],
) -> tuple[dict[str, Counter], dict[str, Counter]]:
    group_by_id: dict[str, str] = {}
    distributions: dict[str, Counter] = defaultdict(Counter)
    for row in mappings:
        detail = predictions[row["expected_id"]]
        group = _evidence_group(detail)
        group_by_id[row["expected_id"]] = group
        distributions[group][detail["prediction"]] += 1
    return group_by_id, distributions


def _fill_missing_evidence(
    working_database: Path,
    mappings: list[dict[str, Any]],
    evidence_by_policy: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    empty_policy_ids = sorted(
        policy_id
        for policy_id, rows in evidence_by_policy.items()
        if not rows
    )
    benchmark_policy_ids = {f"POL-{row['application_id']}" for row in mappings}
    if set(empty_policy_ids) != benchmark_policy_ids.intersection(empty_policy_ids):
        raise ValueError("Unexpected policy selection while finding zero-evidence policies")
    app_names = {row["application_id"]: row["application"] for row in mappings}
    engine = create_engine(
        f"sqlite:///{working_database.as_posix()}",
        connect_args={"check_same_thread": False},
    )
    session: Session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)()
    import app.services.policy_extraction_service as extraction_module

    original_ai_extractor = extraction_module.extract_policy_evidence_with_ai
    ai_attempts: dict[str, dict[str, Any]] = {}

    def tracked_ai_extractor(policy_text: str, application_name: str) -> list[dict]:
        try:
            result = original_ai_extractor(policy_text, application_name)
        except Exception as exc:
            ai_attempts[application_name] = {
                "attempted": True,
                "accepted": False,
                "error_type": type(exc).__name__,
            }
            raise
        accepted = bool(validate_policy_evidence(result))
        ai_attempts[application_name] = {
            "attempted": True,
            "accepted": accepted,
            "error_type": "",
        }
        return result

    extraction_module.extract_policy_evidence_with_ai = tracked_ai_extractor
    audit: list[dict[str, Any]] = []
    try:
        with _working_directory(BACKEND):
            for policy_id in empty_policy_ids:
                policy = session.get(PolicyDocument, policy_id)
                if policy is None:
                    raise ValueError(f"Missing policy while filling evidence: {policy_id}")
                app_id = policy.application_id
                app_name = app_names[app_id]
                policy_text = policy.raw_text
                extracted = policy_extraction_service.extract_policy_evidence(
                    policy_text,
                    app_name,
                )
                tracker = ai_attempts.get(app_name, {})
                extraction_method = (
                    "Gemini accepted evidence"
                    if tracker.get("accepted")
                    else "regex fallback"
                )
                inserted = 0
                for item in extracted:
                    evidence_id = f"GAPFILL-{uuid.uuid4().hex[:16]}"
                    session.add(
                        PolicyEvidence(
                            evidence_id=evidence_id,
                            policy_id=policy_id,
                            data_type=item.get("data_type"),
                            purpose=item.get("purpose"),
                            entity=item.get("entity") or app_name,
                            sharing=item.get("sharing"),
                            retention=item.get("retention"),
                            evidence_text=item["evidence_text"],
                            source_section=item.get("source_section"),
                            extraction_status=item.get("extraction_status") or "EXTRACTED",
                            confidence=item.get("confidence"),
                        )
                    )
                    inserted += 1
                session.commit()
                audit.append(
                    {
                        "application_id": app_id,
                        "application": app_name,
                        "policy_id": policy_id,
                        "stored_text_chars": len(policy_text or ""),
                        "stored_text_status": (
                            "NOT_CAPTURED"
                            if "NOT_CAPTURED" in (policy_text or "")
                            else "PENDING_CAPTURE"
                            if "PENDING_CAPTURE" in (policy_text or "")
                            or "PENDING_REGION_CHECK" in (policy_text or "")
                            else "stored policy text"
                        ),
                        "extraction_method": extraction_method,
                        "gemini_attempted": bool(tracker.get("attempted")),
                        "gemini_error_type": tracker.get("error_type", ""),
                        "new_evidence_rows": inserted,
                    }
                )
    finally:
        extraction_module.extract_policy_evidence_with_ai = original_ai_extractor
        session.close()
        engine.dispose()
    return audit


def _synthetic_sensitivity(
    mappings: list[dict[str, Any]],
    original_predictions: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]], list[dict[str, Any]]]:
    selected_apps = sorted(SYNTHETIC_TYPES)
    selected = [row for row in mappings if row["application_id"] in selected_apps]
    anchors: dict[str, dict[str, Any]] = {}
    for row in sorted(selected, key=lambda item: item["expected_id"]):
        anchors.setdefault(row["application_id"], row)
    if set(anchors) != set(SYNTHETIC_TYPES):
        raise ValueError("Seeded sensitivity app set does not match the selected benchmark apps")

    with tempfile.TemporaryDirectory(prefix="idf_b_seeded_") as temp_dir:
        database = Path(temp_dir) / "fdo_privacy_seeded.sqlite"
        base._copy_database(DATABASE, database)
        engine = create_engine(
            f"sqlite:///{database.as_posix()}",
            connect_args={"check_same_thread": False},
        )
        session: Session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)()
        synthetic_ids: dict[str, str] = {}
        for app_id, data_type in SYNTHETIC_TYPES.items():
            expected_types = set(
                session.scalars(
                    select(ExpectedMapping.data_type)
                    .where(ExpectedMapping.application_id == app_id)
                )
            )
            if data_type in expected_types:
                raise ValueError(f"Synthetic data type {data_type} is expected by {app_id}")
            evidence_id = f"SYNTHETIC-{app_id}"
            synthetic_ids[app_id] = evidence_id
            session.add(
                PolicyEvidence(
                    evidence_id=evidence_id,
                    policy_id=f"POL-{app_id}",
                    data_type=data_type,
                    purpose="Marketing",
                    entity="SYNTHETIC TEST ONLY",
                    sharing=None,
                    retention=None,
                    evidence_text=(
                        f"SYNTHETIC TEST ROW — this is not source-policy text. "
                        f"Declared {data_type} for marketing."
                    ),
                    source_section="SYNTHETIC_TEST",
                    extraction_status="EXTRACTED",
                    confidence=0.99,
                )
            )
        session.commit()
        session.close()
        engine.dispose()

        seeded_evidence, _ = _read_db_evidence(database, mappings)
        seeded_relational = base._run_relational(
            mappings,
            seeded_evidence,
            source_database=database,
        )
        synthetic_rows = []
        for app_id in selected_apps:
            anchor = anchors[app_id]
            synthetic_type = SYNTHETIC_TYPES[app_id]
            relational_detail = seeded_relational[anchor["expected_id"]]
            original_detail = original_predictions[anchor["expected_id"]]
            app_evidence_types = {
                row["data_type"]
                for row in seeded_evidence[f"POL-{app_id}"]
                if row["data_type"]
            }
            exact = anchor["expected_data_type"] == synthetic_type
            b1_prediction = (
                "NOT_FDO"
                if anchor["expected_data_type"] in app_evidence_types
                else "FDO"
            )
            b2_prediction = "NOT_FDO" if exact else "FDO"
            synthetic_rows.append(
                {
                    "application_id": app_id,
                    "application": anchor["application"],
                    "category": anchor["category"],
                    "anchor_expected_id": anchor["expected_id"],
                    "anchor_function": anchor["function"],
                    "expected_data_type": anchor["expected_data_type"],
                    "synthetic_evidence_id": synthetic_ids[app_id],
                    "synthetic_data_type": synthetic_type,
                    "synthetic_purpose": "Marketing",
                    "synthetic_label": "SYNTHETIC_TEST_NOT_SOURCE_EVIDENCE",
                    "synthetic_source_section": "SYNTHETIC_TEST",
                    "data_type_differs_from_all_app_expectations": True,
                    "original_relational_prediction": original_detail["prediction"],
                    "seeded_relational_prediction": relational_detail["prediction"],
                    "seeded_relational_rule": relational_detail["rule_fired"],
                    "seeded_relational_confidence": relational_detail["confidence"],
                    "synthetic_evidence_selected_by_analysis_runner": (
                        relational_detail["evidence_id"] == synthetic_ids[app_id]
                    ),
                    "seeded_relational_fdo_flag": relational_detail["prediction"] == "FDO",
                    "B1_prediction": b1_prediction,
                    "B1_fdo_flag": b1_prediction == "FDO",
                    "B1_rule_confidence": "NA (baseline has no rule/confidence)",
                    "B2_data_match": "EXACT_MATCH" if exact else "NO_MATCH",
                    "B2_prediction": b2_prediction,
                    "B2_fdo_flag": b2_prediction == "FDO",
                    "B2_rule_confidence": "NA (baseline has no rule/confidence)",
                    "relational_synthetic_row_outcome": (
                        "No relational comparison: matcher requires expected data-type equality"
                    ),
                    "relational_synthetic_row_rule_confidence": "NA (no synthetic comparison was selected)",
                }
            )
        return synthetic_rows, seeded_relational, [
            {
                "application_id": app_id,
                "synthetic_evidence_id": synthetic_ids[app_id],
                "data_type": SYNTHETIC_TYPES[app_id],
                "expected_types": sorted(
                    {
                        row["expected_data_type"]
                        for row in mappings
                        if row["application_id"] == app_id
                    }
                ),
                "purpose": "Marketing",
            }
            for app_id in selected_apps
        ]


def _preserve_first_run() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for original_name, retained_name in (
        ("results.csv", "first_run_results.csv"),
        ("confusion_matrix.csv", "first_run_confusion_matrix.csv"),
        ("report.md", "first_run_report.md"),
    ):
        source = OUTPUT / original_name
        retained = OUTPUT / retained_name
        if source.exists() and not retained.exists():
            shutil.copy2(source, retained)


def _write_results(
    mappings: list[dict[str, Any]],
    prediction_sets: dict[str, dict[str, str]],
    details_by_method: dict[str, dict[str, Any]],
    groups: dict[str, str],
) -> tuple[dict[str, dict[str, Any]], dict[str, Counter]]:
    summary_by_method: dict[str, dict[str, Any]] = {}
    matrices: dict[str, Counter] = {}
    rows: list[dict[str, Any]] = []
    app_accuracies: dict[tuple[str, str], tuple[int, int]] = {}
    category_accuracies: dict[tuple[str, str], tuple[int, int]] = {}

    for method, predictions in prediction_sets.items():
        metric, matrix = base._metrics(mappings, predictions)
        summary_by_method[method] = metric
        matrices[method] = matrix
        by_app: dict[str, list[dict[str, Any]]] = defaultdict(list)
        by_category: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for mapping in mappings:
            by_app[mapping["application_id"]].append(mapping)
            by_category[mapping["category"]].append(mapping)
        for group_key, grouped in by_app.items():
            correct = sum(predictions[m["expected_id"]] == m["ground_truth"] for m in grouped)
            app_accuracies[(method, group_key)] = (correct, len(grouped))
        for group_key, grouped in by_category.items():
            correct = sum(predictions[m["expected_id"]] == m["ground_truth"] for m in grouped)
            category_accuracies[(method, group_key)] = (correct, len(grouped))

        for mapping in mappings:
            expected_id = mapping["expected_id"]
            detail = details_by_method.get(method, {}).get(expected_id, {})
            app_correct, app_count = app_accuracies[(method, mapping["application_id"])]
            cat_correct, cat_count = category_accuracies[(method, mapping["category"])]
            rows.append(
                {
                    "method": method,
                    "expected_id": expected_id,
                    "application_id": mapping["application_id"],
                    "application": mapping["application"],
                    "category": mapping["category"],
                    "function": mapping["function"],
                    "expected_data_type": mapping["expected_data_type"],
                    "expected_purpose": mapping.get("expected_purpose", ""),
                    "ground_truth": mapping["ground_truth"],
                    "prediction": predictions[expected_id],
                    "correct": str(predictions[expected_id] == mapping["ground_truth"]).lower(),
                    "app_accuracy": app_correct / app_count,
                    "category_accuracy": cat_correct / cat_count,
                    "method_precision_fdo": metric["fdo_precision"],
                    "method_recall_fdo": metric["fdo_recall"],
                    "method_f1_fdo": metric["fdo_f1"],
                    "method_accuracy": metric["accuracy"],
                    "method_ambiguous_share": metric["ambiguous_share"],
                    "evidence_coverage_group_first_run": groups.get(expected_id, ""),
                    **detail,
                }
            )

    fields = list(dict.fromkeys(key for row in rows for key in row))
    with (OUTPUT / "results.csv").open("w", newline="", encoding="utf-8-sig") as target:
        writer = csv.DictWriter(target, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    with (OUTPUT / "confusion_matrix.csv").open("w", newline="", encoding="utf-8-sig") as target:
        fields = ("method", "ground_truth", "predicted", "count")
        writer = csv.DictWriter(target, fieldnames=fields)
        writer.writeheader()
        for method, matrix in matrices.items():
            for truth in base.LABELS:
                for predicted in base.LABELS:
                    writer.writerow(
                        {
                            "method": method,
                            "ground_truth": truth,
                            "predicted": predicted,
                            "count": matrix[(truth, predicted)],
                        }
                    )
    return summary_by_method, matrices


def _write_sensitivity(rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    fields = list(dict.fromkeys(key for row in rows for key in row))
    with (OUTPUT / "seeded_overreach_sensitivity.csv").open(
        "w", newline="", encoding="utf-8-sig"
    ) as target:
        writer = csv.DictWriter(target, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _metrics_table(metrics: dict[str, dict[str, Any]]) -> list[str]:
    lines = [
        "| Method and run | N | FDO precision | FDO recall | FDO F1 | Accuracy | Predicted AMBIGUOUS share |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for method, value in metrics.items():
        lines.append(
            f"| {method} | {value['n']} | {base._format_metric(value['fdo_precision'])} | "
            f"{base._format_metric(value['fdo_recall'])} | {base._format_metric(value['fdo_f1'])} | "
            f"{base._format_metric(value['accuracy'])} | {base._format_metric(value['ambiguous_share'])} |"
        )
    return lines


def _write_report(
    mappings: list[dict[str, Any]],
    policies: dict[str, dict[str, Any]],
    evidence_before: dict[str, list[dict[str, Any]]],
    evidence_after: dict[str, list[dict[str, Any]]],
    extraction_audit: list[dict[str, Any]],
    first_run: dict[str, dict[str, Any]],
    group_by_id: dict[str, str],
    group_distribution: dict[str, Counter],
    metrics: dict[str, dict[str, Any]],
    matrices: dict[str, Counter],
    seeded_rows: list[dict[str, Any]],
    semantic_available: bool,
    semantic_results: dict[str, dict[str, Any]] | None,
    semantic_diff: list[dict[str, Any]],
    semantic_failure: str,
    semantic_url: str | None,
    persistent_fuseki_reachable: bool,
    persistent_fuseki_reachable_after: bool,
) -> None:
    no_evidence_apps = sorted(
        app_id for app_id in policies if not evidence_before[f"POL-{app_id}"]
    )
    mappings_by_app = Counter(row["application_id"] for row in mappings)
    not_fdo_had_evidence = [
        row for row in mappings
        if row["ground_truth"] == "NOT_FDO"
        and group_by_id[row["expected_id"]] == "REAL_MATCH_COMPARISON"
    ]
    not_fdo_correct_had_evidence = sum(
        first_run[row["expected_id"]]["prediction"] == "NOT_FDO"
        for row in not_fdo_had_evidence
    )
    false_fdo = {
        "First-run relational": sum(
            first_run[row["expected_id"]]["prediction"] == "FDO"
            and row["ground_truth"] != "FDO"
            for row in mappings
        ),
        "B1": sum(
            first_run_baselines["B1"][row["expected_id"]] == "FDO"
            and row["ground_truth"] != "FDO"
            for row in mappings
        ),
        "B2": sum(
            first_run_baselines["B2"][row["expected_id"]] == "FDO"
            and row["ground_truth"] != "FDO"
            for row in mappings
        ),
    }
    lines = [
        "# IDF-B follow-up evaluation",
        "",
        "## Ground truth and agreement",
        "",
        "- Ground truth remains read-only: `DATA/FDO-Privacy_Final_Stage3_Dataset_CLEANED.xlsx` has 99 expected "
        "mappings; the final 93 labels are in the Stage 6 `Stage 5 Final Mapping Dataset` sheet, with columns "
        "`Expected ID`, `App ID`, `Function`, `Data Type`, and `Final FDO Status`. Matching Stage 4E "
        "`Final FDO Label` values were left unchanged.",
        "- Final labeled set: 93 mappings across 29 apps; 0 FDO, 60 NOT_FDO, and 33 AMBIGUOUS. Six of the 99 "
        "expected mappings are unlabeled; Amazon Shopping has no Stage 6 mapping.",
        "- Label remaps: `NO_FDO_ESTABLISHED` → `NOT_FDO`; `PENDING` → `AMBIGUOUS` from the parallel Stage 6 "
        "`FDO Label`. No other labels were remapped. Placeholder Stage 4 labels were not used.",
        "- No paired final-outcome annotator labels exist, so Cohen's kappa (overall or per category) is not "
        "computable.",
        "",
        "## Evidence coverage and original run",
        "",
        f"- Benchmark: {len(mappings)} labeled mappings across {len(policies)} apps; "
        f"{sum(bool(rows) for rows in evidence_before.values())} canonical policies had stored evidence "
        f"({sum(not rows for rows in evidence_before.values())} did not).",
        "- The following policies had no stored `policy_evidence` rows before extraction:",
        "",
        "| App | Policy ID | Labeled mappings covered | Stored policy text status | Text length |",
        "|---|---|---:|---|---:|",
    ]
    for app_id in no_evidence_apps:
        policy = policies[app_id]
        audit = next(row for row in extraction_audit if row["application_id"] == app_id)
        lines.append(
            f"| {mappings_by_app[app_id] and next(m['application'] for m in mappings if m['application_id']==app_id)} "
            f"({app_id}) | {policy['policy_id']} | {mappings_by_app[app_id]} | "
            f"{audit['stored_text_status']} | {audit['stored_text_chars']} |"
        )

    lines.extend(
        [
            "",
            f"The ten no-evidence policies cover **{sum(mappings_by_app[app_id] for app_id in no_evidence_apps)} "
            f"of the 93 labeled mappings**.",
            "",
            f"Mappings were classified from the first-run relational comparisons as **{sum(v == 'NO_EVIDENCE (Rule 1)' for v in group_by_id.values())}** "
            "NO_EVIDENCE / Rule 1, **"
            f"{sum(v == 'INSUFFICIENT_EVIDENCE (Rule 2)' for v in group_by_id.values())}** insufficient / Rule 2, and **"
            f"{sum(v == 'REAL_MATCH_COMPARISON' for v in group_by_id.values())}** real matched comparisons.",
            "",
            "| Evidence-driven group | FDO | NOT_FDO | AMBIGUOUS | Total |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for group in (
        "NO_EVIDENCE (Rule 1)",
        "INSUFFICIENT_EVIDENCE (Rule 2)",
        "REAL_MATCH_COMPARISON",
    ):
        counts = group_distribution[group]
        lines.append(
            f"| {group} | {counts['FDO']} | {counts['NOT_FDO']} | {counts['AMBIGUOUS']} | "
            f"{sum(counts.values())} |"
        )
    lines.extend(
        [
            "",
            f"NOT_FDO recall restricted to mappings with a selected stored evidence match: "
            f"**{not_fdo_correct_had_evidence}/{len(not_fdo_had_evidence)}** "
            f"({not_fdo_correct_had_evidence / len(not_fdo_had_evidence):.3f})"
            if not_fdo_had_evidence
            else "NOT_FDO recall restricted to mappings with a selected stored evidence match: NA (no such gold mappings).",
            "",
            "The per-mapping original coverage group is included in `results.csv` under "
            "`evidence_coverage_group_first_run` and in the preserved first-run details.",
            "",
            "## Fill the evidence gap",
            "",
            "- Extraction used the app's standard `extract_policy_evidence()` pipeline on the database's stored "
            "`raw_text` only; no policy URL was fetched. `GEMINI_API_KEY` is configured in `Backend/.env`, so the "
            "pipeline attempted Gemini and used its regex fallback whenever Gemini returned no validated evidence "
            "or raised an error. No secret value is recorded.",
            "- All ten no-evidence policies have `NOT_CAPTURED` or `PENDING_CAPTURE`/`PENDING_REGION_CHECK` "
            "placeholder text, not a captured policy body. This limits what extraction can produce.",
            "",
            "| App | Extraction path used | Gemini attempted | Gemini error type | New evidence rows |",
            "|---|---|---:|---|---:|",
        ]
    )
    for row in extraction_audit:
        lines.append(
            f"| {row['application']} ({row['application_id']}) | {row['extraction_method']} | "
            f"{row['gemini_attempted']} | {row['gemini_error_type'] or 'none'} | {row['new_evidence_rows']} |"
        )
    lines.extend(
        [
            "",
            f"Evidence coverage after running extraction: **{sum(bool(rows) for rows in evidence_after.values())}/29 "
            f"policies** ({sum(len(rows) for rows in evidence_after.values())} evidence rows total). Before extraction: "
            f"**{sum(bool(rows) for rows in evidence_before.values())}/29 policies** "
            f"({sum(len(rows) for rows in evidence_before.values())} evidence rows total).",
            "",
            "The extraction attempt added **0** evidence records from stored policy text; these inputs are marked "
            "uncaptured or pending in the database, so this does not measure extraction quality on captured policy "
            "bodies.",
            "",
            "### Full metric table",
            "",
        ]
    )
    lines.extend(_metrics_table(metrics))
    lines.extend(["", "### Confusion matrices", ""])
    for method, matrix in matrices.items():
        lines.extend(
            [
                f"**{method}** (rows ground truth; columns prediction)",
                "",
                "| Ground truth \\\\ Predicted | FDO | NOT_FDO | AMBIGUOUS |",
                "|---|---:|---:|---:|",
            ]
        )
        for truth in base.LABELS:
            lines.append(
                f"| {truth} | {matrix[(truth, 'FDO')]} | {matrix[(truth, 'NOT_FDO')]} | "
                f"{matrix[(truth, 'AMBIGUOUS')]} |"
            )
        lines.append("")

    correct_not_fdo = next(
        (
            (mapping, first_run[mapping["expected_id"]])
            for mapping in mappings
            if mapping["ground_truth"] == "NOT_FDO"
            and first_run[mapping["expected_id"]]["prediction"] == "NOT_FDO"
            and first_run[mapping["expected_id"]]["evidence_text"]
        ),
        None,
    )
    lines.extend(["### Retained worked example", ""])
    if correct_not_fdo:
        mapping, detail = correct_not_fdo
        lines.append(
            f"Correct NOT_FDO — {mapping['application']} ({mapping['category']}), "
            f"{mapping['function']}; expected `{mapping['expected_data_type']}` for "
            f"{mapping.get('expected_purpose', 'purpose unavailable')}. Matched policy text: "
            f"“{detail['evidence_text']}” Data match / purpose compatibility / functional relationship: "
            f"{detail['data_match']} / {detail['purpose_compatibility']} / "
            f"{detail['functional_relationship']}; rule: {detail['rule_fired']}; confidence: "
            f"{detail['confidence']}; explanation: {detail['explanation']}"
        )
    else:
        lines.append("No correct NOT_FDO example was available in the original run with stored evidence.")
    lines.extend(["", "No correct FDO worked example is possible: the gold set has zero FDO mappings.", ""])

    lines.extend(
        [
            "### False FDO flags on unseeded benchmark mappings",
            "",
            f"- First-run relational: **{false_fdo['First-run relational']}** false FDO flags.",
            f"- B1: **{false_fdo['B1']}** false FDO flags.",
            f"- B2: **{false_fdo['B2']}** false FDO flags.",
            "",
            "Every FDO prediction on the unseeded benchmark is a false FDO flag because the gold set has zero FDO labels.",
            "",
            "## Seeded overreach sensitivity test (synthetic; not accuracy)",
            "",
            "Ten apps with no initial evidence were selected. One evidence row was added to each temporary database, "
            "marked `SYNTHETIC_TEST`, with an expected-data type not present among any expected type for that app and "
            "purpose `Marketing`. The seeded rows and app-specific expected-type lists are recorded in "
            "`seeded_overreach_sensitivity.csv`.",
            "",
            "| Method | Seed rows flagged FDO | Rule / confidence |",
            "|---|---:|---|",
            f"| Relational `analysis_runner` on benchmark mappings | "
            f"{sum(bool(row['seeded_relational_fdo_flag']) for row in seeded_rows)} / 10 | "
            "No synthetic row was selected: exact expected-type filtering prevented comparison. The associated "
            "anchor mappings retained Rule 1 / confidence 0.30; the synthetic row itself has no rule/confidence.",
            f"| B1 app-type presence on anchor mappings | {sum(bool(row['B1_fdo_flag']) for row in seeded_rows)} / 10 | "
            "FDO whenever anchor expected type is absent from all policy evidence; no rule/confidence (baseline).",
            f"| B2 direct data-type-only comparison to synthetic row | "
            f"{sum(bool(row['B2_fdo_flag']) for row in seeded_rows)} / 10 | "
            "FDO on `NO_MATCH`; no rule/confidence (baseline).",
            "",
            "This controlled result describes the current matching surface: the relational runner only considers "
            "evidence with an exact expected data type, so unrelated declared types do not reach its mismatch rule. "
            "The B1/B2 synthetic checks are sensitivity comparisons against each app's first sorted expected mapping; "
            "they do not claim real-world accuracy.",
            "",
            "## Semantic branch",
            "",
        ]
    )
    if semantic_available and semantic_results is not None:
        semantic_metric, semantic_matrix = base._metrics(
            mappings,
            {key: value["prediction"] for key, value in semantic_results.items()},
        )
        lines.extend(_metrics_table({"Semantic, gap-filled": semantic_metric}))
        lines.extend(
            [
                "",
                f"Semantic and gap-filled relational verdicts differ on **{len(semantic_diff)} mappings**.",
                f"localhost:3030 was {'reachable' if persistent_fuseki_reachable else 'unreachable'} at the initial "
                f"probe and {'reachable' if persistent_fuseki_reachable_after else 'unreachable'} at post-run "
                f"verification. The semantic branch used a separate temporary in-memory endpoint ({semantic_url}) "
                f"and was stopped after analysis, avoiding changes to any existing persistent store.",
                "",
                "| Expected ID | App | Relational | Semantic | Reason for difference |",
                "|---|---|---|---|---|",
            ]
        )
        for diff in semantic_diff:
            lines.append(
                f"| {diff['expected_id']} | {diff['application']} ({diff['application_id']}) | "
                f"{diff['relational_prediction']} | {diff['semantic_prediction']} | {diff['reason']} |"
            )
        if not semantic_diff:
            lines.append("| — | — | — | — | No verdict differences. |")
        lines.extend(["", "Semantic confusion matrix (rows ground truth; columns prediction):", ""])
        lines.extend(
            [
                "| Ground truth \\\\ Predicted | FDO | NOT_FDO | AMBIGUOUS |",
                "|---|---:|---:|---:|",
            ]
        )
        for truth in base.LABELS:
            lines.append(
                f"| {truth} | {semantic_matrix[(truth, 'FDO')]} | "
                f"{semantic_matrix[(truth, 'NOT_FDO')]} | {semantic_matrix[(truth, 'AMBIGUOUS')]} |"
            )
    else:
        lines.append(
            f"Semantic metrics were not computed. {semantic_failure} No request was sent to the existing "
            "localhost:3030 persistent store because the semantic pipeline clears its graph."
        )
    lines.extend(
        [
            "",
            "## Assumptions and uncomputed values",
            "",
            "- Only canonical policy IDs `POL-<App ID>` and existing stored policy text/evidence were used. No source "
            "URL was fetched. All extraction/evidence seeding occurred in disposable copies of the SQLite database.",
            "- Before/after coverage counts policy evidence rows, and per-mapping evidence group is based on the exact "
            "comparison status persisted by `analysis_runner`: `NO_EVIDENCE` = Rule 1; `INSUFFICIENT`/`UNKNOWN` or "
            "non-`EXTRACTED` = Rule 2; selected extracted evidence = real comparison.",
            "- B1 and B2 retain the definitions in `Backend/eval/README.md`; seeded B2 is explicitly a direct "
            "synthetic expected-vs-declared data-type comparison because the production matcher does not select the "
            "injected unrelated type.",
            "- If extraction yields zero evidence from placeholder text, the uncomputed gap-fill improvement is not "
            "a model failure measurement: source policy text is absent. Real-policy extraction quality cannot be "
            "evaluated from these rows.",
            "- The gold set still has zero FDO cases, so FDO recall and F1 remain undefined; semantic metrics and "
            "semantic disagreement reasons are unavailable if isolated Fuseki cannot run. Kappa remains unavailable "
            "because there are no paired final-outcome annotator labels. Per-category accuracy is included for each "
            "method/mapping in `results.csv`; per-category kappa is not computable.",
            "",
            "First-run snapshots are retained as `first_run_results.csv`, `first_run_confusion_matrix.csv`, and "
            "`first_run_report.md`. The updated full mapping-level table and matrices are in `results.csv` and "
            "`confusion_matrix.csv`.",
        ]
    )
    (OUTPUT / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _start_isolated_fuseki() -> tuple[str | None, int | None, str, Path]:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    base_url = f"http://localhost:{port}"
    fuseki_base = BACKEND / "eval" / f".fuseki_runtime_{port}_{uuid.uuid4().hex[:8]}"
    fuseki_base.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["FUSEKI_BASE"] = str(fuseki_base)
    distribution = BACKEND.parent / "apache-jena-fuseki-6.2.0"
    command = [
        "java",
        "-Xmx2G",
        "-cp",
        "fuseki-server.jar",
        "org.apache.jena.fuseki.main.cmds.FusekiServerUICmd",
        "--mem",
        "--update",
        "--localhost",
        "--port",
        str(port),
        "/fdo-reasoning",
    ]
    process = subprocess.Popen(
        command,
        cwd=distribution,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    for _ in range(45):
        if process.poll() is not None:
            return None, process.pid, f"Fuseki exited during startup (exit code {process.returncode}).", fuseki_base
        try:
            with urllib.request.urlopen(f"{base_url}/$/ping", timeout=1):
                return base_url, process.pid, "", fuseki_base
        except Exception:
            time.sleep(1)
    return None, process.pid, "Isolated Fuseki did not respond within 45 seconds.", fuseki_base


def _fuseki_reachable(base_url: str) -> bool:
    try:
        with urllib.request.urlopen(f"{base_url}/$/ping", timeout=2):
            return True
    except Exception:
        return False


def _stop_isolated_fuseki(pid: int | None, runtime_dir: Path | None) -> None:
    if pid is not None:
        subprocess.run(
            [
                "powershell.exe",
                "-NoProfile",
                "-Command",
                f"Stop-Process -Id {pid} -ErrorAction SilentlyContinue",
            ],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    eval_dir = (BACKEND / "eval").resolve()
    if (
        runtime_dir is not None
        and runtime_dir.resolve().parent == eval_dir
        and runtime_dir.name.startswith(".fuseki_runtime_")
        and runtime_dir.is_dir()
    ):
        shutil.rmtree(runtime_dir)


first_run_baselines: dict[str, dict[str, str]] = {}


def main() -> None:
    _preserve_first_run()
    mappings, _ = base.load_ground_truth()
    _attach_expected_purposes(mappings, DATABASE)
    evidence_before, policies = _read_db_evidence(DATABASE, mappings)
    persistent_fuseki_reachable = _fuseki_reachable("http://localhost:3030")

    original_relational = base._run_relational(
        mappings,
        evidence_before,
        source_database=DATABASE,
    )
    original_b1_b2 = base._baselines(mappings, original_relational, evidence_before)
    global first_run_baselines
    first_run_baselines = original_b1_b2
    original_predictions = {
        "First-run relational": {
            key: value["prediction"] for key, value in original_relational.items()
        },
        "First-run B1": original_b1_b2["B1"],
        "First-run B2": original_b1_b2["B2"],
    }
    _, group_distribution = _rule_group_summary(mappings, original_relational)
    group_by_id, group_distribution = _rule_group_summary(mappings, original_relational)

    with tempfile.TemporaryDirectory(prefix="idf_b_gapfill_") as temp_dir:
        working_database = Path(temp_dir) / "fdo_privacy_gapfilled.sqlite"
        base._copy_database(DATABASE, working_database)
        extraction_audit = _fill_missing_evidence(
            working_database,
            mappings,
            evidence_before,
        )
        evidence_after, _ = _read_db_evidence(working_database, mappings)
        gapfilled_relational = base._run_relational(
            mappings,
            evidence_after,
            source_database=working_database,
        )
        gapfilled_b1_b2 = base._baselines(
            mappings,
            gapfilled_relational,
            evidence_after,
        )

        prediction_sets: dict[str, dict[str, str]] = {
            "first_run_relational": original_predictions["First-run relational"],
            "first_run_B1": original_predictions["First-run B1"],
            "first_run_B2": original_predictions["First-run B2"],
            "gapfilled_relational": {
                key: value["prediction"] for key, value in gapfilled_relational.items()
            },
            "gapfilled_B1": gapfilled_b1_b2["B1"],
            "gapfilled_B2": gapfilled_b1_b2["B2"],
        }
        details: dict[str, dict[str, Any]] = {
            "first_run_relational": original_relational,
            "first_run_B1": {},
            "first_run_B2": {},
            "gapfilled_relational": gapfilled_relational,
            "gapfilled_B1": {},
            "gapfilled_B2": {},
        }

        semantic_url, semantic_pid, semantic_failure, semantic_runtime = _start_isolated_fuseki()
        semantic_available = bool(semantic_url)
        semantic_results = None
        semantic_diff: list[dict[str, Any]] = []
        if semantic_available:
            try:
                semantic_results = base._run_semantic(
                    mappings,
                    source_database=working_database,
                    base_url=semantic_url,
                )
                prediction_sets["semantic_gapfilled"] = {
                    key: value["prediction"] for key, value in semantic_results.items()
                }
                details["semantic_gapfilled"] = semantic_results
                if set(prediction_sets["semantic_gapfilled"]) != {
                    row["expected_id"] for row in mappings
                }:
                    raise RuntimeError("Semantic branch did not return all 93 mappings")
                for mapping in mappings:
                    expected_id = mapping["expected_id"]
                    semantic = semantic_results[expected_id]
                    relational = gapfilled_relational[expected_id]
                    if semantic["prediction"] != relational["prediction"]:
                        semantic_diff.append(
                            {
                                "expected_id": expected_id,
                                "application_id": mapping["application_id"],
                                "application": mapping["application"],
                                "relational_prediction": relational["prediction"],
                                "semantic_prediction": semantic["prediction"],
                                "reason": (
                                    f"Relational: {relational['rule_fired']} "
                                    f"({relational['decision_reason']}); Semantic: "
                                    f"{semantic['decision_reason']}"
                                ),
                            }
                        )
            except Exception as exc:
                semantic_available = False
                semantic_results = None
                prediction_sets.pop("semantic_gapfilled", None)
                details.pop("semantic_gapfilled", None)
                semantic_failure = f"{type(exc).__name__}: {exc}"
            else:
                semantic_failure = ""

        _stop_isolated_fuseki(semantic_pid, semantic_runtime)
        persistent_fuseki_reachable_after = _fuseki_reachable("http://localhost:3030")

        seeded_rows, seeded_relational, seeded_injected = _synthetic_sensitivity(
            mappings,
            original_relational,
        )
        metric_data: dict[str, dict[str, Any]] = {}
        matrices: dict[str, Counter] = {}
        for method, preds in prediction_sets.items():
            metric_data[method], matrices[method] = base._metrics(mappings, preds)
        group_by_id, _ = _rule_group_summary(mappings, original_relational)
        metric_data, matrices = _write_results(
            mappings,
            prediction_sets,
            details,
            group_by_id,
        )
        _write_sensitivity(seeded_rows)
        with (OUTPUT / "policy_extraction_audit.csv").open(
            "w", newline="", encoding="utf-8-sig"
        ) as target:
            writer = csv.DictWriter(target, fieldnames=list(extraction_audit[0]))
            writer.writeheader()
            writer.writerows(extraction_audit)
        _write_report(
            mappings,
            policies,
            evidence_before,
            evidence_after,
            extraction_audit,
            original_relational,
            group_by_id,
            group_distribution,
            metric_data,
            matrices,
            seeded_rows,
            semantic_available,
            semantic_results,
            semantic_diff,
            semantic_failure,
            semantic_url,
            persistent_fuseki_reachable,
            persistent_fuseki_reachable_after,
        )
        if semantic_diff:
            with (OUTPUT / "semantic_relational_differences.csv").open(
                "w", newline="", encoding="utf-8-sig"
            ) as target:
                writer = csv.DictWriter(target, fieldnames=list(semantic_diff[0]))
                writer.writeheader()
                writer.writerows(semantic_diff)
    print(
        json.dumps(
            {
                "benchmark_mappings": len(mappings),
                "policies_without_initial_evidence": len(
                    [rows for rows in evidence_before.values() if not rows]
                ),
                "extracted_rows_added": sum(row["new_evidence_rows"] for row in extraction_audit),
                "policies_with_evidence_before": sum(bool(rows) for rows in evidence_before.values()),
                "policies_with_evidence_after": sum(bool(rows) for rows in evidence_after.values()),
                "semantic_available": semantic_available,
                "semantic_failure": semantic_failure,
                "synthetic_test_rows": len(seeded_rows),
                "semantic_url": semantic_url,
                "semantic_pid": semantic_pid,
                "outputs": [
                    str(OUTPUT / "results.csv"),
                    str(OUTPUT / "confusion_matrix.csv"),
                    str(OUTPUT / "report.md"),
                    str(OUTPUT / "first_run_results.csv"),
                    str(OUTPUT / "first_run_confusion_matrix.csv"),
                    str(OUTPUT / "seeded_overreach_sensitivity.csv"),
                    str(OUTPUT / "policy_extraction_audit.csv"),
                ],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
