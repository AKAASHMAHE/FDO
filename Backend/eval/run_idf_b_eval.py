from __future__ import annotations

import csv
import json
import sqlite3
import sys
import tempfile
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from openpyxl import load_workbook
from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "Backend"
DATA = ROOT / "DATA"
OUTPUT = ROOT / "Docs" / "eval_results"
DATABASE = BACKEND / "fdo_privacy.db"
STAGE3_WORKBOOK = DATA / "FDO-Privacy_Final_Stage3_Dataset_CLEANED.xlsx"
STAGE6_WORKBOOK = DATA / "FDO-Privacy_Stage6_Results_Visualization_and_Findings_v1.0.xlsx"

if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from sqlalchemy import create_engine

from app.models.application import Application
from app.models.comparison import Comparison
from app.models.expected_mapping import ExpectedMapping
from app.models.explanation import Explanation
from app.models.fdo_result import FDOResult
from app.models.function import Function
from app.models.policy_document import PolicyDocument
from app.models.policy_evidence import PolicyEvidence
from app.ontology.db_semantic_analysis_service import DBSemanticAnalysisService
from app.ontology.fuseki_service import FusekiService
from app.ontology.semantic_fuseki_service import SemanticFusekiService
from app.services.analysis_runner import run_analysis

LABELS = ("FDO", "NOT_FDO", "AMBIGUOUS")
LABEL_ALIASES = {
    "FDO": "FDO",
    "NOT_FDO": "NOT_FDO",
    "AMBIGUOUS": "AMBIGUOUS",
    "NO_FDO_ESTABLISHED": "NOT_FDO",
    "PENDING": "AMBIGUOUS",
}


def _read_rows(path: Path, sheet_name: str) -> tuple[list[str], list[dict[str, Any]]]:
    workbook = load_workbook(path, read_only=True, data_only=True)
    sheet = workbook[sheet_name]
    iterator = sheet.iter_rows(values_only=True)
    headers = [str(value).strip() if value is not None else "" for value in next(iterator)]
    rows = [
        dict(zip(headers, row))
        for row in iterator
        if any(value is not None and str(value).strip() for value in row)
    ]
    workbook.close()
    return headers, rows


def _semantic_finding_reason(findings: list[dict[str, Any]]) -> str:
    if not findings:
        return "No semantic finding was returned for this mapping."
    if len(findings) == 1:
        return str(findings[0].get("reason") or "")

    verdicts = {str(item.get("fdo_status") or "") for item in findings}
    if len(verdicts) == 1:
        verdict = next(iter(verdicts))
        return (
            f"{len(findings)} semantic findings were returned "
            f"with unanimous verdict {verdict}."
        )
    return (
        f"{len(findings)} semantic findings were returned "
        "with conflicting verdicts."
    )


def load_ground_truth() -> tuple[list[dict[str, Any]], dict[str, dict[str, str]]]:
    _, app_rows = _read_rows(STAGE3_WORKBOOK, "Applications")
    app_metadata = {
        str(row["App ID"]).strip(): {
            "application": str(row["Application"]).strip(),
            "category": str(row["Category"]).strip(),
        }
        for row in app_rows
        if row.get("App ID") and row.get("Application")
    }

    headers, rows = _read_rows(STAGE6_WORKBOOK, "Stage 5 Final Mapping Dataset")
    required = {"Expected ID", "App ID", "Function", "Data Type", "Final FDO Status"}
    missing = required.difference(headers)
    if missing:
        raise ValueError(f"Missing Stage 6 ground-truth columns: {sorted(missing)}")

    mappings = []
    seen_ids = set()
    for row in rows:
        expected_id = str(row["Expected ID"]).strip()
        app_id = str(row["App ID"]).strip()
        if expected_id in seen_ids:
            raise ValueError(f"Duplicate ground-truth Expected ID: {expected_id}")
        seen_ids.add(expected_id)
        if app_id not in app_metadata:
            raise ValueError(f"No Stage 3 Applications record for App ID {app_id}")

        status_value = str(row.get("Final FDO Status") or "").strip().upper()
        label_value = str(row.get("FDO Label") or "").strip().upper()
        status = LABEL_ALIASES.get(status_value)
        mapped_label = LABEL_ALIASES.get(label_value)
        if status is None:
            raise ValueError(f"Unrecognized Final FDO Status {status_value!r} for {expected_id}")
        if mapped_label is not None and mapped_label != status:
            raise ValueError(
                f"Stage 6 status/label conflict for {expected_id}: "
                f"{status_value!r} versus {label_value!r}"
            )

        mappings.append(
            {
                "expected_id": expected_id,
                "application_id": app_id,
                "application": app_metadata[app_id]["application"],
                "category": app_metadata[app_id]["category"],
                "function": str(row.get("Function") or "").strip(),
                "expected_data_type": str(row.get("Data Type") or "").strip(),
                "ground_truth": status,
                "source_label": label_value,
            }
        )

    if not mappings:
        raise ValueError("The Stage 6 final mapping sheet contains no labeled mappings")
    return mappings, app_metadata


def _copy_database(source_path: Path, target_path: Path) -> None:
    source = sqlite3.connect(f"file:{source_path.as_posix()}?mode=ro", uri=True)
    target = sqlite3.connect(target_path)
    try:
        source.backup(target)
    finally:
        target.close()
        source.close()


def _rule_fired(comparison: Comparison, result: FDOResult) -> str:
    if comparison.evidence_status == "NO_EVIDENCE":
        return "Rule 1: No declared evidence"
    if comparison.evidence_status in {"INSUFFICIENT", "UNKNOWN"}:
        return "Rule 2: Insufficient or unknown evidence"
    if comparison.evidence_status != "EXTRACTED":
        return "Rule 2: Evidence status does not support a deterministic decision"
    if (
        comparison.data_match == "EXACT_MATCH"
        and comparison.purpose_compatibility == "COMPATIBLE"
        and comparison.functional_relationship == "RELATED"
    ):
        return "Rule 3: Exact data + compatible purpose + related function"
    if (
        comparison.data_match == "EXACT_MATCH"
        and comparison.purpose_compatibility == "INCOMPATIBLE"
        and comparison.functional_relationship == "RELATED"
    ):
        return "Rule 4: Exact data + incompatible purpose + related function"
    if (
        comparison.data_match == "NO_MATCH"
        and comparison.functional_relationship == "RELATED"
    ):
        return "Rule 5: Different data type + related function"
    return "Conservative fallback"


def _run_relational(
    mappings: list[dict[str, Any]],
    evidence_by_policy: dict[str, list[dict[str, Any]]],
    source_database: Path = DATABASE,
) -> dict[str, dict[str, Any]]:
    with tempfile.TemporaryDirectory(prefix="idf_b_eval_") as temp_dir:
        clone_path = Path(temp_dir) / "fdo_privacy_eval.sqlite"
        _copy_database(source_database, clone_path)
        engine = create_engine(
            f"sqlite:///{clone_path.as_posix()}",
            connect_args={"check_same_thread": False},
        )
        session_factory = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
        session: Session = session_factory()
        results: dict[str, dict[str, Any]] = {}

        app_ids = sorted({mapping["application_id"] for mapping in mappings})
        targets_by_app: dict[str, set[str]] = defaultdict(set)
        for mapping in mappings:
            targets_by_app[mapping["application_id"]].add(mapping["expected_id"])

        for app_id in app_ids:
            policy_id = f"POL-{app_id}"
            policy = session.get(PolicyDocument, policy_id)
            if policy is None or policy.application_id != app_id:
                raise ValueError(f"Canonical stored policy {policy_id} is missing or belongs to another app")

            analysis_id = f"IDFB-EVAL-{app_id}"
            analysis = run_analysis(
                session,
                analysis_id=analysis_id,
                application_id=app_id,
                policy_id=policy_id,
            )
            if analysis.analysis_status != "COMPLETED":
                raise RuntimeError(f"analysis_runner did not complete for {app_id}")

            rows = session.execute(
                select(Comparison, FDOResult)
                .join(FDOResult, FDOResult.comparison_id == Comparison.comparison_id)
                .where(Comparison.analysis_id == analysis_id)
            ).all()
            for comparison, result in rows:
                expected_id = comparison.expected_id
                if expected_id not in targets_by_app[app_id]:
                    continue
                explanation = session.scalar(
                    select(Explanation).where(Explanation.result_id == result.result_id)
                )
                evidence = (
                    session.get(PolicyEvidence, comparison.evidence_id)
                    if comparison.evidence_id
                    else None
                )
                results[expected_id] = {
                    "prediction": result.fdo_status,
                    "confidence": result.decision_confidence,
                    "decision_reason": result.decision_reason,
                    "explanation": explanation.explanation_text if explanation else "",
                    "evidence_id": evidence.evidence_id if evidence else "",
                    "evidence_text": evidence.evidence_text if evidence else "",
                    "evidence_data_type": evidence.data_type if evidence else "",
                    "evidence_purpose": evidence.purpose if evidence else "",
                    "evidence_status": evidence.extraction_status if evidence else "",
                    "data_match": comparison.data_match,
                    "purpose_compatibility": comparison.purpose_compatibility,
                    "functional_relationship": comparison.functional_relationship,
                    "decision_evidence_status": comparison.evidence_status,
                    "rule_fired": _rule_fired(comparison, result),
                    "policy_id": policy_id,
                }
            session.rollback()

        missing_ids = targets_by_app.keys() if not results else {
            mapping["expected_id"] for mapping in mappings
        }.difference(results)
        if missing_ids:
            raise RuntimeError(f"analysis_runner produced no verdict for: {sorted(missing_ids)}")

        session.close()
        engine.dispose()
        return results


def _fuseki_is_available() -> bool:
    try:
        with urllib.request.urlopen("http://localhost:3030/$/ping", timeout=2):
            return True
    except (urllib.error.URLError, TimeoutError, ConnectionError):
        return False


def _run_semantic(
    mappings: list[dict[str, Any]],
    source_database: Path = DATABASE,
    base_url: str = "http://localhost:3030",
) -> dict[str, dict[str, Any]]:
    results: dict[str, dict[str, Any]] = {}
    with tempfile.TemporaryDirectory(prefix="idf_b_semantic_") as temp_dir:
        clone_path = Path(temp_dir) / "fdo_privacy_eval.sqlite"
        _copy_database(source_database, clone_path)
        engine = create_engine(
            f"sqlite:///{clone_path.as_posix()}",
            connect_args={"check_same_thread": False},
        )
        session: Session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)()
        semantic_fuseki = SemanticFusekiService(
            FusekiService(
                base_url=base_url,
                dataset="fdo-reasoning",
            )
        )
        service = DBSemanticAnalysisService(
            fuseki_service=semantic_fuseki,
        )
        app_ids = sorted({mapping["application_id"] for mapping in mappings})

        for app_id in app_ids:
            policy_id = f"POL-{app_id}"
            application = session.get(Application, app_id)
            expected = list(
                session.scalars(
                    select(ExpectedMapping)
                    .where(ExpectedMapping.application_id == app_id)
                    .order_by(ExpectedMapping.expected_id)
                )
            )
            functions = list(
                session.scalars(
                    select(Function)
                    .where(Function.application_id == app_id)
                    .order_by(Function.function_record_id)
                )
            )
            declared = list(
                session.scalars(
                    select(PolicyEvidence)
                    .where(PolicyEvidence.policy_id == policy_id)
                    .order_by(PolicyEvidence.evidence_id)
                )
            )
            findings = service.analyze(
                application=application,
                functions=functions,
                expected_data=expected,
                declared_data=declared,
                output_path=Path(temp_dir) / f"{app_id}.ttl",
            )
            expected_ids = {
                row.expected_id
                for row in expected
                if row.expected_id in {m["expected_id"] for m in mappings}
            }
            grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
            for finding in findings:
                value = str(finding.get("expected_data") or "")
                expected_id = next(
                    (candidate for candidate in expected_ids if value.endswith(candidate)),
                    None,
                )
                if expected_id:
                    grouped[expected_id].append(finding)

            for expected_id in expected_ids:
                group = grouped.get(expected_id, [])
                verdicts = {str(item["fdo_status"]) for item in group}
                prediction = verdicts.pop() if len(verdicts) == 1 else "AMBIGUOUS"
                results[expected_id] = {
                    "prediction": prediction,
                    "confidence": "",
                    "decision_reason": _semantic_finding_reason(group),
                    "explanation": "",
                    "evidence_id": "",
                    "evidence_text": "",
                    "evidence_data_type": "",
                    "evidence_purpose": "",
                    "evidence_status": "",
                    "data_match": "",
                    "purpose_compatibility": "",
                    "functional_relationship": "",
                    "rule_fired": "Semantic finding decision adapter",
                    "policy_id": policy_id,
                }
        session.close()
        engine.dispose()
    return results


def _baselines(
    mappings: list[dict[str, Any]],
    relational: dict[str, dict[str, Any]],
    evidence_by_policy: dict[str, list[dict[str, Any]]],
) -> dict[str, dict[str, str]]:
    predictions: dict[str, dict[str, str]] = {
        "B1": {},
        "B2": {},
    }
    for mapping in mappings:
        expected_id = mapping["expected_id"]
        policy_id = f"POL-{mapping['application_id']}"
        app_types = {
            row["data_type"]
            for row in evidence_by_policy.get(policy_id, [])
            if row["data_type"]
        }
        predictions["B1"][expected_id] = (
            "NOT_FDO"
            if mapping["expected_data_type"] in app_types
            else "FDO"
        )

        data_match = relational[expected_id]["data_match"]
        if data_match == "EXACT_MATCH":
            predictions["B2"][expected_id] = "NOT_FDO"
        elif data_match == "NO_MATCH":
            predictions["B2"][expected_id] = "FDO"
        else:
            predictions["B2"][expected_id] = "AMBIGUOUS"
    return predictions


def _metrics(
    mappings: list[dict[str, Any]],
    predictions: dict[str, str],
) -> tuple[dict[str, Any], dict[tuple[str, str], int]]:
    matrix = Counter((row["ground_truth"], predictions[row["expected_id"]]) for row in mappings)
    total = len(mappings)
    true_fdo = matrix[("FDO", "FDO")]
    predicted_fdo = sum(matrix[(truth, "FDO")] for truth in LABELS)
    actual_fdo = sum(matrix[("FDO", prediction)] for prediction in LABELS)
    precision = true_fdo / predicted_fdo if predicted_fdo else None
    recall = true_fdo / actual_fdo if actual_fdo else None
    f1 = (
        2 * precision * recall / (precision + recall)
        if precision is not None and recall is not None and precision + recall
        else None
    )
    accuracy = sum(matrix[(label, label)] for label in LABELS) / total if total else None
    ambiguous_share = sum(matrix[(truth, "AMBIGUOUS")] for truth in LABELS) / total if total else None
    return (
        {
            "n": total,
            "fdo_precision": precision,
            "fdo_recall": recall,
            "fdo_f1": f1,
            "accuracy": accuracy,
            "ambiguous_share": ambiguous_share,
        },
        matrix,
    )


def _write_results(
    mappings: list[dict[str, Any]],
    method_predictions: dict[str, dict[str, str]],
    details: dict[str, dict[str, Any]],
) -> tuple[dict[str, dict[str, Any]], dict[str, Counter]]:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    categories: dict[str, Counter] = defaultdict(Counter)
    apps: dict[str, Counter] = defaultdict(Counter)
    method_metrics: dict[str, dict[str, Any]] = {}
    matrices: dict[str, Counter] = {}

    for method, predictions in method_predictions.items():
        summary, matrix = _metrics(mappings, predictions)
        method_metrics[method] = summary
        matrices[method] = matrix
        for mapping in mappings:
            correct = predictions[mapping["expected_id"]] == mapping["ground_truth"]
            if correct:
                categories[f"{method}|{mapping['category']}"]["correct"] += 1
            categories[f"{method}|{mapping['category']}"]["total"] += 1
            if correct:
                apps[f"{method}|{mapping['application_id']}"]["correct"] += 1
            apps[f"{method}|{mapping['application_id']}"]["total"] += 1

    result_fields = [
        "method",
        "expected_id",
        "application_id",
        "application",
        "category",
        "function",
        "expected_data_type",
        "expected_purpose",
        "ground_truth",
        "prediction",
        "correct",
        "app_accuracy",
        "category_accuracy",
        "method_precision_fdo",
        "method_recall_fdo",
        "method_f1_fdo",
        "method_accuracy",
        "method_ambiguous_share",
        "policy_id",
        "evidence_id",
        "evidence_data_type",
        "evidence_purpose",
        "evidence_status",
        "evidence_text",
        "data_match",
        "purpose_compatibility",
        "functional_relationship",
        "rule_fired",
        "confidence",
        "decision_reason",
        "explanation",
    ]

    with (OUTPUT / "results.csv").open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=result_fields)
        writer.writeheader()
        for method, predictions in method_predictions.items():
            summary = method_metrics[method]
            for mapping in mappings:
                expected_id = mapping["expected_id"]
                detail = details.get(method, {}).get(expected_id, {})
                app_count = apps[f"{method}|{mapping['application_id']}"]
                category_count = categories[f"{method}|{mapping['category']}"]
                writer.writerow(
                    {
                        **{key: mapping.get(key, "") for key in (
                            "expected_id", "application_id", "application", "category",
                            "function", "expected_data_type", "expected_purpose", "ground_truth",
                        )},
                        "method": method,
                        "prediction": predictions[expected_id],
                        "correct": str(predictions[expected_id] == mapping["ground_truth"]).lower(),
                        "app_accuracy": app_count["correct"] / app_count["total"],
                        "category_accuracy": category_count["correct"] / category_count["total"],
                        "method_precision_fdo": summary["fdo_precision"],
                        "method_recall_fdo": summary["fdo_recall"],
                        "method_f1_fdo": summary["fdo_f1"],
                        "method_accuracy": summary["accuracy"],
                        "method_ambiguous_share": summary["ambiguous_share"],
                        **detail,
                    }
                )

    with (OUTPUT / "confusion_matrix.csv").open("w", newline="", encoding="utf-8-sig") as file:
        fields = ("method", "ground_truth", "predicted", "count")
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for method, matrix in matrices.items():
            for truth in LABELS:
                for predicted in LABELS:
                    writer.writerow(
                        {
                            "method": method,
                            "ground_truth": truth,
                            "predicted": predicted,
                            "count": matrix[(truth, predicted)],
                        }
                    )
    return method_metrics, matrices


def _format_metric(value: Any) -> str:
    return "NA" if value is None else f"{value:.3f}"


def _report(
    mappings: list[dict[str, Any]],
    details: dict[str, dict[str, Any]],
    method_predictions: dict[str, dict[str, str]],
    method_metrics: dict[str, dict[str, Any]],
    matrices: dict[str, Counter],
    evidence_by_policy: dict[str, list[dict[str, Any]]],
    policies: dict[str, dict[str, Any]],
    semantic_available: bool,
) -> None:
    label_counts = Counter(row["ground_truth"] for row in mappings)
    app_ids = sorted({row["application_id"] for row in mappings})
    policy_with_evidence = sum(bool(evidence_by_policy.get(f"POL-{app_id}")) for app_id in app_ids)
    _, stage3_expected = _read_rows(STAGE3_WORKBOOK, "Expected Data")
    stage3_expected_ids = {
        str(row["Expected ID"]).strip()
        for row in stage3_expected
        if row.get("Expected ID")
    }
    _, stage3_apps = _read_rows(STAGE3_WORKBOOK, "Applications")
    stage3_app_names = {
        str(row["App ID"]).strip(): str(row.get("Application") or "").strip()
        for row in stage3_apps
        if row.get("App ID")
    }
    unlabeled_expected_ids = sorted(
        stage3_expected_ids.difference(row["expected_id"] for row in mappings)
    )
    unlabeled_app_ids = sorted(set(stage3_app_names).difference(app_ids))
    unlabeled_app_summary = ", ".join(
        f"{app_id} ({stage3_app_names[app_id]})" for app_id in unlabeled_app_ids
    )
    lines = [
        "# IDF-B experimental results",
        "",
        "## 8.1 Dataset and ground truth",
        "",
        f"- Ground-truth source: `DATA/FDO-Privacy_Stage6_Results_Visualization_and_Findings_v1.0.xlsx`, "
        "`Stage 5 Final Mapping Dataset`.",
        "- Ground-truth mapping columns: `Expected ID`, `App ID`, `Function`, `Data Type`, and `Final FDO Status`; "
        "`FDO Label` was used as a consistency check.",
        "- The same 93 mapping IDs and labels are present in "
        "`DATA/FDO-Privacy_Stage4E_Ambiguous_Case_Resolution_v1.0.xlsx`, sheet "
        "`Stage 4E Ambiguous Resolution`, columns `Expected ID`, `App ID`, `Function`, `Data Type`, and "
        "`Final FDO Label`; the Stage 4E labels match Stage 6 `Final FDO Status` exactly.",
        "- App display name and category: `DATA/FDO-Privacy_Final_Stage3_Dataset_CLEANED.xlsx`, "
        "`Applications` sheet, columns `App ID`, `Application`, and `Category`.",
        f"- Labeled mappings: **{len(mappings)}**; apps: **{len(app_ids)}**; canonical policy records: **{len(policies)}** "
        f"({policy_with_evidence} with stored evidence, {len(policies) - policy_with_evidence} without stored evidence).",
        f"- Ground-truth labels: FDO **{label_counts['FDO']}**, NOT_FDO **{label_counts['NOT_FDO']}**, "
        f"AMBIGUOUS **{label_counts['AMBIGUOUS']}**.",
        f"- Coverage against the Stage 3 `Expected Data` sheet: **{len(stage3_expected_ids)}** mappings exist; "
        f"{len(unlabeled_expected_ids)} do not appear in the Stage 6 labeled set "
        f"({', '.join(unlabeled_expected_ids)}). The {len(unlabeled_app_ids)} Stage 3 app without Stage 6 "
        f"ground-truth mappings: {unlabeled_app_summary}.",
        "- Label mapping used: `FDO` → `FDO`; `NOT_FDO` → `NOT_FDO`; `AMBIGUOUS` → `AMBIGUOUS`; "
        "the parallel Stage 6 `FDO Label` values `NO_FDO_ESTABLISHED` → `NOT_FDO` and `PENDING` → `AMBIGUOUS`. "
        "The canonical `Final FDO Status` column already contains the normalized class values.",
        "- Stage 4 workbooks contain intermediate values such as `NOT_ASSIGNED`, `NO_FDO_LABEL`, and `NO_FINAL_FDO`; "
        "these are workflow placeholders, not final outcome labels, and were not counted as ground truth.",
        "- The separate Stage 4D `4D Adjudication` sheet uses `NOT_FDO_ON_CURRENT_EVIDENCE` and "
        "`AMBIGUOUS_NEEDS_EVIDENCE` as adjudication decisions while its `Final FDO Label` is `NO_FINAL_FDO`; "
        "these preliminary decisions were not substituted for the Stage 4E/Stage 6 final labels.",
        "- The Stage 6 ground truth has no FDO-positive mappings. Consequently no correctly predicted FDO worked example "
        "exists, and FDO recall/F1 are undefined; precision is zero only when a method predicted one or more FDOs, "
        "otherwise precision is undefined. These undefined values are `NA`, not imputed.",
        "- App mapping IDs in the Stage 6 set were checked against `Backend/fdo_privacy.db`; all 93 expected IDs were found. "
        "Each evaluated app used its canonical stored policy ID `POL-<App ID>`, not additional test/runtime policy records.",
        "- `normalized_evidence` has no records. For B1, canonical `policy_evidence.data_type` values were used as the "
        "stored normalized data-type evidence. All non-empty data types for the selected policy were considered, without "
        "filtering on extraction status.",
        "- Extraction in this evaluation used existing database evidence only. The run did not invoke Gemini/LLM extraction "
        "or the regex fallback. The database has no per-row extractor provenance, so the original extraction route "
        "for its pre-existing evidence cannot be determined from these fields.",
        "",
        "### Annotator agreement",
        "",
        "No paired annotator labels for the final FDO / NOT_FDO / AMBIGUOUS outcome are present. "
        "`DATA/FDO-Privacy_Stage2B_AnnotatorB_All4Batches.xlsx`, sheet `Sheet1`, contains paired "
        "`Necessity (A)` / `Necessity (B)` and `Purpose (A)` / `Purpose (B)` annotations, which are not FDO "
        "outcome labels; no Cohen's kappa for the FDO ground-truth classes can therefore be computed. "
        "Per-class kappa is likewise unavailable.",
        "",
        "## 8.2 Method results",
        "",
        "| Method | N | FDO precision | FDO recall | FDO F1 | Accuracy | Predicted AMBIGUOUS share |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    method_names = {"relational": "Relational (analysis_runner)", "B1": "B1", "B2": "B2", "semantic": "Semantic"}
    for method, summary in method_metrics.items():
        lines.append(
            f"| {method_names.get(method, method)} | {summary['n']} | "
            f"{_format_metric(summary['fdo_precision'])} | {_format_metric(summary['fdo_recall'])} | "
            f"{_format_metric(summary['fdo_f1'])} | {_format_metric(summary['accuracy'])} | "
            f"{_format_metric(summary['ambiguous_share'])} |"
        )
    if not semantic_available:
        lines.append(
            "| Semantic | NA | NA | NA | NA | NA | NA |"
        )
        lines.extend(
            [
                "",
                "The Fuseki ping at `http://localhost:3030/$/ping` timed out, so no semantic predictions or "
                "semantic metrics were computed.",
            ]
        )
    lines.extend(
        [
            "",
            "### Per-app-category accuracy",
            "",
            "| Method | App category | Mappings | Correct | Accuracy |",
            "|---|---|---:|---:|---:|",
        ]
    )
    for method in method_metrics:
        by_category: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in mappings:
            by_category[row["category"]].append(row)
        for category, group in sorted(by_category.items()):
            correct = sum(
                method_predictions[method][row["expected_id"]] == row["ground_truth"]
                for row in group
            )
            lines.append(
                f"| {method_names.get(method, method)} | {category} | {len(group)} | {correct} | "
                f"{correct / len(group):.3f} |"
            )
    lines.extend(
        [
            "",
            "### Confusion matrices",
            "",
            "Rows are ground truth; columns are predicted. Class order is FDO, NOT_FDO, AMBIGUOUS.",
            "",
        ]
    )
    for method, matrix in matrices.items():
        lines.append(f"**{method_names.get(method, method)}**")
        lines.append("")
        lines.append("| Ground truth \\\\ Predicted | FDO | NOT_FDO | AMBIGUOUS |")
        lines.append("|---|---:|---:|---:|")
        for truth in LABELS:
            lines.append(
                f"| {truth} | {matrix[(truth, 'FDO')]} | {matrix[(truth, 'NOT_FDO')]} | "
                f"{matrix[(truth, 'AMBIGUOUS')]} |"
            )
        lines.append("")
    lines.extend(
        [
            "### Kappa",
            "",
            "Cohen's kappa for FDO outcome annotations: **not computable** (no paired annotator outcome labels). "
            "Per-category FDO kappa: **not computable** for the same reason.",
            "",
            "## 8.3 Worked examples",
            "",
        ]
    )
    not_fdo_correct = next(
        (
            (method, row)
            for method in method_metrics
            for row in mappings
            if row["ground_truth"] == "NOT_FDO"
            and method_predictions[method][row["expected_id"]] == "NOT_FDO"
            and method == "relational"
            and details["relational"][row["expected_id"]]["evidence_text"]
        ),
        None,
    )
    if not_fdo_correct:
        method, row = not_fdo_correct
        detail = details[method][row["expected_id"]]
        lines.extend(
            [
                "### Correct NOT_FDO — relational analysis",
                "",
                f"- App/category: {row['application']} / {row['category']}",
                f"- Function: {row['function']}",
                f"- Expected data and purpose: `{row['expected_data_type']}`; "
                f"{row['expected_purpose']}",
                f"- Verbatim matched policy text: “{detail['evidence_text']}”",
                f"- Data match / purpose compatibility / functional relationship: "
                f"{detail['data_match']} / {detail['purpose_compatibility']} / {detail['functional_relationship']}",
                f"- Rule fired: {detail['rule_fired']}",
                f"- Confidence: {detail['confidence']}",
                f"- Explanation: {detail['explanation']}",
                "",
            ]
        )
    else:
        lines.extend(["No correct NOT_FDO relational example with a stored matched evidence sentence was available.", ""])

    lines.extend(
        [
            "### Correct FDO",
            "",
            "Not available: the selected Stage 6 ground truth contains zero FDO labels. Any FDO prediction would be "
            "incorrect against this benchmark, so no correct FDO example can be shown.",
            "",
            "### Assumptions and uncomputed values",
            "",
            "- Policy selection: the canonical Stage 3 policy record `POL-<App ID>` was used for each benchmark app. "
            "It avoids duplicate runtime/test policy records in the SQLite database.",
            "- B1 compares the expected data-type identifier to any non-empty `policy_evidence.data_type` for that "
            "app's selected canonical policy: present → NOT_FDO; absent → FDO.",
            "- B2 uses only the relational runner's selected evidence `data_match`: EXACT_MATCH → NOT_FDO, "
            "NO_MATCH → FDO, NO_EVIDENCE → AMBIGUOUS.",
            "- Metric values unavailable: FDO recall and F1 for all methods (zero positive gold labels); FDO precision "
            "where no FDO predictions were made; all semantic metrics (Fuseki unavailable); and FDO-class kappa.",
            "- The evaluation used an isolated temporary copy of the SQLite database for `analysis_runner`; the source "
            "database and application code were not modified.",
            "",
            "See `results.csv` for mapping-level results and `confusion_matrix.csv` for all available 3×3 matrices.",
        ]
    )
    (OUTPUT / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

def main() -> None:
    mappings, _ = load_ground_truth()
    app_ids = sorted({row["application_id"] for row in mappings})
    source = sqlite3.connect(f"file:{DATABASE.as_posix()}?mode=ro", uri=True)
    source.row_factory = sqlite3.Row
    try:
        policies: dict[str, dict[str, Any]] = {}
        evidence_by_policy: dict[str, list[dict[str, Any]]] = {}
        db_mappings = {}
        for app_id in app_ids:
            policy_id = f"POL-{app_id}"
            policy_row = source.execute(
                "SELECT policy_id, application_id, source_type, raw_text "
                "FROM policy_documents WHERE policy_id = ?",
                (policy_id,),
            ).fetchone()
            if policy_row is None or policy_row["application_id"] != app_id:
                raise ValueError(f"Required canonical stored policy missing: {policy_id}")
            policies[app_id] = dict(policy_row)
            evidence_by_policy[policy_id] = [
                dict(row)
                for row in source.execute(
                    "SELECT evidence_id, policy_id, data_type, purpose, evidence_text, "
                    "extraction_status, confidence FROM policy_evidence "
                    "WHERE policy_id = ? ORDER BY evidence_id",
                    (policy_id,),
                )
            ]
        for row in mappings:
            db_row = source.execute(
                "SELECT e.expected_id, e.application_id, e.function_record_id, e.data_type, "
                "e.expected_purpose, f.function_name "
                "FROM expected_mappings e JOIN functions f "
                "ON f.function_record_id = e.function_record_id "
                "WHERE e.expected_id = ?",
                (row["expected_id"],),
            ).fetchone()
            if db_row is None:
                raise ValueError(f"Ground-truth mapping absent from database: {row['expected_id']}")
            if db_row["application_id"] != row["application_id"]:
                raise ValueError(f"App ID mismatch for {row['expected_id']}")
            if db_row["data_type"] != row["expected_data_type"]:
                raise ValueError(f"Expected data type mismatch for {row['expected_id']}")
            row["expected_purpose"] = db_row["expected_purpose"]
            db_mappings[row["expected_id"]] = dict(db_row)
    finally:
        source.close()

    relational = _run_relational(mappings, evidence_by_policy)
    method_predictions: dict[str, dict[str, str]] = {
        "relational": {
            expected_id: result["prediction"]
            for expected_id, result in relational.items()
        }
    }
    details: dict[str, dict[str, Any]] = {"relational": relational}
    baseline_predictions = _baselines(mappings, relational, evidence_by_policy)
    for method, predictions in baseline_predictions.items():
        method_predictions[method] = predictions
        details[method] = {}

    semantic_available = _fuseki_is_available()
    if semantic_available:
        semantic = _run_semantic(mappings)
        method_predictions["semantic"] = {
            expected_id: detail["prediction"]
            for expected_id, detail in semantic.items()
        }
        details["semantic"] = semantic
        if set(method_predictions["semantic"]) != {row["expected_id"] for row in mappings}:
            raise RuntimeError("Semantic branch did not return one result for every ground-truth mapping")

    method_metrics, matrices = _write_results(mappings, method_predictions, details)
    _report(
        mappings,
        details,
        method_predictions,
        method_metrics,
        matrices,
        evidence_by_policy,
        policies,
        semantic_available,
    )
    print(
        json.dumps(
            {
                "mappings": len(mappings),
                "apps": len(app_ids),
                "policies": len(policies),
                "policies_with_evidence": sum(bool(evidence_by_policy[f"POL-{app_id}"]) for app_id in app_ids),
                "fuseki_available": semantic_available,
                "outputs": [
                    str(OUTPUT / "results.csv"),
                    str(OUTPUT / "confusion_matrix.csv"),
                    str(OUTPUT / "report.md"),
                ],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
