from __future__ import annotations

import csv
import re
import sqlite3
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "Backend"
DATA = ROOT / "DATA"
OUTPUT = ROOT / "Docs" / "eval_results" / "diagnostics" / "report.md"
DATABASE = BACKEND / "fdo_privacy.db"
STAGE3 = DATA / "FDO-Privacy_Final_Stage3_Dataset_CLEANED.xlsx"
FIRST_RUN = ROOT / "Docs" / "eval_results" / "first_run_results.csv"
SEMANTIC_DIFFS = ROOT / "Docs" / "eval_results" / "semantic_relational_differences.csv"

sys.path.insert(0, str(BACKEND))
from app.services.comparison_service import (  # noqa: E402
    classify_purpose,
    classify_purposes,
    normalize_purpose,
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_sheet(path: Path, sheet_name: str) -> list[dict[str, Any]]:
    workbook = load_workbook(path, read_only=True, data_only=True)
    try:
        sheet = workbook[sheet_name]
        rows = sheet.iter_rows(values_only=True)
        headers = [str(value or "").strip() for value in next(rows)]
        return [
            {headers[index]: value for index, value in enumerate(row) if index < len(headers)}
            for row in rows
            if any(value is not None for value in row)
        ]
    finally:
        workbook.close()


def db_connect() -> sqlite3.Connection:
    connection = sqlite3.connect(
        f"file:{DATABASE.as_posix()}?mode=ro",
        uri=True,
    )
    connection.row_factory = sqlite3.Row
    return connection


def esc(value: Any) -> str:
    text = "" if value is None else str(value)
    return text.replace("|", "\\|").replace("\r", " ").replace("\n", " ").strip()


def code_normalization(value: Any) -> str:
    """Diagnostic-only alias hypothesis; production code remains unchanged."""
    code = str(value or "").strip().upper()
    if code.startswith("DATA.COMM."):
        code = "DATA.COM." + code[len("DATA.COMM.") :]
    return code


def purpose_root_cause(expected: str, declared: str) -> str:
    expected_norm = normalize_purpose(expected)
    declared_norm = normalize_purpose(declared)
    expected_category = classify_purpose(expected)
    declared_categories = classify_purposes(declared)
    if expected_norm == declared_norm:
        return "Normalization behavior inconsistent with exact-normalized equality (verify)"
    if expected_category is None or not declared_categories:
        return "Taxonomy coverage gap: at least one purpose is unclassified"
    if expected_category not in declared_categories:
        if "localization" in expected_norm or "localization" in declared_norm:
            return (
                "Taxonomy gap/collision: `localization` is not a taxonomy term; "
                "the declared `security` clause wins classification"
            )
        return "Purpose mismatch under current taxonomy (distinct classified categories)"
    return "No mismatch predicted by current compatibility code (verify stored result)"


def list_pairs(expected_types: set[str], database_types: set[str]) -> list[tuple[str, str]]:
    workbook_normalized: dict[str, list[str]] = defaultdict(list)
    db_normalized: dict[str, list[str]] = defaultdict(list)
    for value in sorted(expected_types):
        workbook_normalized[code_normalization(value)].append(value)
    for value in sorted(database_types):
        db_normalized[code_normalization(value)].append(value)

    pairs: set[tuple[str, str]] = set()
    for normalized in workbook_normalized.keys() & db_normalized.keys():
        all_values = set(workbook_normalized[normalized]) | set(db_normalized[normalized])
        for left in all_values:
            for right in all_values:
                if left < right and left != right:
                    pairs.add((left, right))
    return sorted(pairs)


def main() -> None:
    expected_rows = read_sheet(STAGE3, "Expected Data")
    workbook_types = {
        str(row.get("Data Type ID") or "").strip()
        for row in expected_rows
        if str(row.get("Data Type ID") or "").strip()
    }
    first_rows = read_csv(FIRST_RUN)
    relational = {
        row["expected_id"]: row
        for row in first_rows
        if row["method"] == "relational"
    }
    semantic_diff_rows = read_csv(SEMANTIC_DIFFS)

    connection = db_connect()
    try:
        expected_db_types = {
            str(row[0]).strip()
            for row in connection.execute(
                "SELECT DISTINCT data_type FROM expected_mappings "
                "WHERE data_type IS NOT NULL AND TRIM(data_type) <> ''"
            )
        }
        all_evidence_type_rows = connection.execute(
            "SELECT data_type, COUNT(*) AS row_count FROM policy_evidence "
            "GROUP BY data_type ORDER BY data_type"
        ).fetchall()
        all_evidence_types = {
            str(row["data_type"]).strip()
            for row in all_evidence_type_rows
            if row["data_type"] is not None and str(row["data_type"]).strip()
        }
        extra_evidence_types = sorted(all_evidence_types - expected_db_types)

        expected_type_code_mismatches = sorted(
            value for value in workbook_types ^ expected_db_types
        )
        apps: dict[str, dict[str, Any]] = {}
        evidence_by_app: dict[str, list[dict[str, Any]]] = {}
        mapping_apps = {
            row["application_id"]: row
            for row in first_rows
            if row["method"] == "relational"
        }
        for app_id, sample in mapping_apps.items():
            policy_id = f"POL-{app_id}"
            policy = connection.execute(
                "SELECT policy_id, application_id, source_identifier, document_name, raw_text "
                "FROM policy_documents WHERE policy_id = ?",
                (policy_id,),
            ).fetchone()
            if policy is None:
                raise ValueError(f"Missing canonical policy record {policy_id}")
            apps[app_id] = dict(policy) | {
                "application": sample["application"],
                "category": sample["category"],
            }
            evidence_by_app[app_id] = [
                dict(row)
                for row in connection.execute(
                    "SELECT evidence_id, data_type, purpose, evidence_text, extraction_status "
                    "FROM policy_evidence WHERE policy_id = ? ORDER BY evidence_id",
                    (policy_id,),
                )
            ]

        rule1_rows = [
            row
            for row in relational.values()
            if row["rule_fired"].startswith("Rule 1")
            and evidence_by_app[row["application_id"]]
        ]
        expected_by_id = {
            str(row.get("Expected ID") or "").strip(): row
            for row in expected_rows
        }
        normalized_matches: dict[str, list[str]] = {}
        for row in rule1_rows:
            expected = row["expected_data_type"]
            normalized_matches[row["expected_id"]] = sorted(
                {
                    str(evidence["data_type"])
                    for evidence in evidence_by_app[row["application_id"]]
                    if evidence["data_type"]
                    and code_normalization(evidence["data_type"])
                    == code_normalization(expected)
                }
            )

        rule4_rows = [
            row
            for row in relational.values()
            if row["prediction"] == "FDO"
        ]

        semantic_rows = {
            row["expected_id"]: row
            for row in read_csv(ROOT / "Docs" / "eval_results" / "results.csv")
            if row["method"] == "semantic_gapfilled"
        }
        no_unique = [
            row
            for row in semantic_rows.values()
            if "No unique semantic finding was returned" in row["decision_reason"]
        ]
    finally:
        connection.close()

    lines: list[str] = [
        "# IDF-B diagnostic report",
        "",
        "Diagnostic-only, read-only inspection of application source, Stage 3 workbook labels/data, and "
        "`Backend/fdo_privacy.db`. No application code, workbook, or database was changed. The only generated "
        "artifacts are this report and the diagnostic script under the permitted folders.",
        "",
        "## 1. Type-code consistency",
        "",
        f"Stage 3 `Expected Data` (`Data Type ID`): **{len(workbook_types)} distinct non-empty codes** across "
        f"{len(expected_rows)} populated rows.",
        "",
        "| Expected Data sheet codes |",
        "|---|",
    ]
    lines.extend(f"| `{esc(value)}` |" for value in sorted(workbook_types))
    lines.extend(
        [
            "",
            f"`expected_mappings.data_type` in SQLite: **{len(expected_db_types)} distinct non-empty codes**. "
            f"Workbook-vs-DB set differences: **{len(expected_type_code_mismatches)}**.",
            "",
            "| Codes present in only one expected-type source |",
            "|---|",
        ]
    )
    lines.extend(
        f"| `{esc(value)}` ({'workbook only' if value in workbook_types else 'DB only'}) |"
        for value in expected_type_code_mismatches
    )
    if not expected_type_code_mismatches:
        lines.append("| None |")
    lines.extend(
        [
            "",
            "Complete `expected_mappings.data_type` set (shared values plus DB-only values):",
            "",
            "| SQLite expected_mappings.data_type |",
            "|---|",
        ]
    )
    lines.extend(f"| `{esc(value)}` |" for value in sorted(expected_db_types))

    aliases = list_pairs(workbook_types, expected_db_types)
    lines.extend(
        [
            "",
            "Near-duplicate diagnostic rule: case/outer-whitespace-insensitive code equality after replacing only "
            "the `DATA.COMM.` namespace prefix with `DATA.COM.`. This is a hypothesis used only for counting; "
            "no stored code was normalized or altered.",
            "",
            "| Near-duplicate spellings |",
            "|---|",
        ]
    )
    lines.extend(f"| `{left}` ↔ `{right}` |" for left, right in aliases)
    if not aliases:
        lines.append("| None under this explicit alias rule |")
    lines.extend(
        [
            "",
            "Additional namespace/granularity warnings (these are not treated as equal codes):",
            "",
            "- Evidence-only `LOCATION`, `LOCATION.PRECISE`, and `precise_location` lack the same canonical "
            "`DATA.LOCATION.PRECISE` spelling/namespace used by expected mappings.",
            "- Evidence types `DATA.ACCOUNT`, `DATA.CONTACTS`, `DATA.DEVICE`, `DATA.FINANCIAL`, `DATA.MEDIA`, "
            "and `DATA.USAGE` are parent/broader codes while expected values include namespaced descendants "
            "(for example `DATA.DEVICE.ID` or `DATA.USAGE.WATCH_HISTORY`).",
            "- `DATA.ACCOUNT.PERSONAL_INFO`, `DATA.CONTACT.PHONE_EMAIL`, `DATA.HEALTH.PERSONAL_HEALTH`, "
            "`DATA.HEALTH.VITALS`, `DATA.MEDIA.AUDIO_VIDEO`, `DATA.USAGE.ACTIVITY_LOGS`, and "
            "`DATA.USAGE.TRIP_DETAILS` are related-sounding but not canonical exact expected codes. Their "
            "semantic equivalence is not assumed.",
            "",
        ]
    )

    evidence_type_counts = {
        str(row["data_type"] or "<NULL>"): int(row["row_count"])
        for row in all_evidence_type_rows
    }
    lines.extend(
        [
            "",
            f"Distinct `policy_evidence.data_type` values across the entire source DB: "
            f"**{len(all_evidence_type_rows)} distinct values**, {len(all_evidence_types)} non-empty.",
            "",
            "| Evidence data_type | Rows |",
            "|---|---:|",
        ]
    )
    lines.extend(
        f"| `{esc(kind)}` | {count} |"
        for kind, count in sorted(evidence_type_counts.items())
    )
    lines.extend(
        [
            "",
            f"Evidence types that never exactly equal a code in `expected_mappings`: "
            f"**{len(extra_evidence_types)}**.",
            "",
            "| Evidence type with no exact expected-type equality |",
            "|---|",
        ]
    )
    lines.extend(f"| `{esc(value)}` |" for value in extra_evidence_types)
    if not extra_evidence_types:
        lines.append("| None |")

    lines.extend(
        [
            "",
            "## 2. Rule 1 despite app-level stored evidence",
            "",
            f"First-run relational rows matching `Rule 1: No declared evidence` where the canonical app policy "
            f"nevertheless has at least one stored evidence row: **{len(rule1_rows)} labeled mappings**.",
            "For each mapping, `app evidence (type — purpose)` lists the canonical policy's distinct type/purpose "
            "pairs. `alias match` uses only the diagnostic `DATA.COMM.` → `DATA.COM.` normalization above.",
            "",
            "| Expected ID | App | Expected type | App evidence (type — purpose) | Alias match |",
            "|---|---|---|---|---|",
        ]
    )
    for row in sorted(rule1_rows, key=lambda item: item["expected_id"]):
        pairs = sorted(
            {
                f"{evidence['data_type'] or '<NULL>'} — {evidence['purpose'] or '<NULL>'}"
                for evidence in evidence_by_app[row["application_id"]]
            }
        )
        lines.append(
            f"| {row['expected_id']} | {esc(row['application'])} ({row['application_id']}) | "
            f"`{esc(row['expected_data_type'])}` | "
            f"{esc('; '.join(pairs))} | "
            f"{esc(', '.join(normalized_matches[row['expected_id']]) or 'none')} |"
        )
    alias_match_count = sum(bool(values) for values in normalized_matches.values())
    no_related_count = len(rule1_rows) - alias_match_count
    lines.extend(
        [
            "",
            f"Under the stated alias normalization, **{alias_match_count}/{len(rule1_rows)}** Rule-1 mappings "
            f"would have a type-equal evidence row. **{no_related_count}/{len(rule1_rows)}** have no "
            "type-related row even after that alias mapping, although every row in this subset's app has some "
            f"stored evidence. Thus **0/{len(rule1_rows)}** have no evidence row at all at the app level; "
            f"**{len(rule1_rows)}/{len(rule1_rows)}** lack a type-equal or alias-equal row. This distinction "
            "matters: Rule 1 is per expected-type lookup, not an app-wide absence-of-evidence test.",
        ]
    )

    lines.extend(
        [
            "",
            "## 3. Rule-4 false FDO predictions",
            "",
            f"The first-run relational output contains **{len(rule4_rows)} FDO predictions**; all are false against "
            "this gold set because it has no FDO labels. Purpose categories below are produced with the app's "
            "existing deterministic purpose classifier; `app category` is the Stage 3 application category.",
            "",
            "| Expected ID | App / app category | Expected purpose / purpose category | Selected evidence purpose / category | Compatibility | Cause under current classifier |",
            "|---|---|---|---|---|---|",
        ]
    )
    for row in sorted(rule4_rows, key=lambda item: item["expected_id"]):
        expected_purpose = row["expected_purpose"] or ""
        declared_purpose = row["evidence_purpose"] or ""
        expected_category = classify_purpose(expected_purpose)
        declared_categories = classify_purposes(declared_purpose)
        lines.append(
            f"| {row['expected_id']} | {esc(row['application'])} ({row['application_id']}; "
            f"{esc(row['category'])}) | {esc(expected_purpose)} / "
            f"`{esc(expected_category or 'UNCLASSIFIED')}` | {esc(declared_purpose)} / "
            f"`{esc(', '.join(declared_categories) or 'UNCLASSIFIED')}` | "
            f"`{esc(row['purpose_compatibility'])}` | "
            f"{esc(purpose_root_cause(expected_purpose, declared_purpose))} |"
        )
    lines.extend(
        [
            "",
            "The code normalizes case, whitespace, and `-`, `_`, `/` separators; then exact normalized text is "
            "compatible. Otherwise it compares one expected category to all categories found in the declared "
            "purpose. If either side is unclassified it returns `INCOMPATIBLE`, not `UNKNOWN`. For the six rows, "
            "five have an unclassified expected purpose; the sixth (`Search/localization` vs a declared purpose "
            "containing `security; localization`) is a taxonomy collision because `localization` is absent from "
            "the controlled phrases and `SECURITY` is selected. None is attributable only to case/separator "
            "normalization, and these outputs do not establish a true human-level purpose mismatch. Relevant code: "
            "[comparison_service.py:176-207](../../../Backend/app/services/comparison_service.py#L176-L207), "
            "[comparison_service.py:313-360](../../../Backend/app/services/comparison_service.py#L313-L360); "
            "Rule 4 decision is [fdo_decision_service.py:101-117](../../../Backend/app/services/fdo_decision_service.py#L101-L117).",
        ]
    )

    lines.extend(
        [
            "",
            "## 4. Unreachable relational Rule 5",
            "",
            "**For the current `analysis_runner` path, `data_match == NO_MATCH` is unreachable.** The matcher filters "
            "the evidence query by both policy ID and exact `PolicyEvidence.data_type == expected.data_type`; an "
            "empty result returns `NO_EVIDENCE`. A selected row necessarily has the same data type as the expected "
            "mapping. When the matcher reports ambiguity it returns `evidence=None`, which again makes comparison "
            "data `NO_EVIDENCE`, not `NO_MATCH`.",
            "",
            "> `PolicyEvidence.data_type == expected.data_type`",
            "",
            "> `if not evidence_rows: ... status=\"NO_EVIDENCE\"`",
            "",
            "Evidence matcher: [evidence_matcher.py:54-75](../../../Backend/app/services/evidence_matcher.py#L54-L75). "
            "The runner passes only `evidence_match.evidence` to comparison at "
            "[analysis_runner.py:150-165](../../../Backend/app/services/analysis_runner.py#L150-L165), and stores "
            "its type at [analysis_runner.py:168-183](../../../Backend/app/services/analysis_runner.py#L168-L183). "
            "`evaluate_data_match` can return `NO_MATCH` for unequal non-empty types "
            "[comparison_service.py:155-175](../../../Backend/app/services/comparison_service.py#L155-L175), but "
            "the exact-type matcher prevents an unequal row from reaching it. The Rule 5 branch exists at "
            "[fdo_decision_service.py:119-136](../../../Backend/app/services/fdo_decision_service.py#L119-L136), "
            "but is unreachable through this runner.",
            "",
            "Thus seeded unrelated evidence is never compared because its type fails the matcher's SQL equality "
            "predicate; no fallback iterates over nonmatching evidence. This is a current selection design, and "
            "it makes the relational Rule 5 branch dead for this production path.",
        ]
    )

    lines.extend(
        [
            "",
            "## 5. Semantic branch vs relational branch",
            "",
            "`FDO_DETECTION_QUERY` matches expected and declared data joined to app/function, and emits a binding "
            "only when the type OR purpose strings differ: "
            "[fdo_detection_queries.py:10-36](../../../Backend/app/ontology/fdo_detection_queries.py#L10-L36). "
            "It therefore does not enumerate equal-type/equal-purpose pairs or create an explicit negative/empty "
            "finding for each expected mapping.",
            "",
            "| SPARQL case | Semantic handling |",
            "|---|---|",
            "| Type-mismatch binding | `semantic_finding_to_decision_input` sets `NO_MATCH` when expected and declared type differ; it sets purpose compatibility from the shared comparator, functional relationship to `RELATED`, and evidence status to `EXTRACTED`. When the policy purpose is compatible and the type differs, FDO Rule 5 returns FDO. See [semantic_decision_adapter.py:15-57](../../../Backend/app/ontology/semantic_decision_adapter.py#L15-L57) and [fdo_decision_service.py:119-136](../../../Backend/app/services/fdo_decision_service.py#L119-L136). |",
            "| No binding for the expected mapping | If the query returns no usable binding for that mapping, the eval harness still creates a result row for every benchmark Expected ID. Its effective binding group is empty, so the verdict set is empty and prediction becomes AMBIGUOUS. Raw findings that fail the app/service usability filter also leave an empty effective group. The reason string is `No unique semantic finding was returned...`. See [db_semantic_result_service.py:216-230](../../../Backend/app/ontology/db_semantic_result_service.py#L216-L230) and [run_idf_b_eval.py:326-336](../../../Backend/eval/run_idf_b_eval.py#L326-L336). |",
            "| Several bindings for the expected mapping | The harness collects distinct `fdo_status` values. If all findings have one common verdict, it returns that verdict even if there are several findings; if verdicts differ, it returns AMBIGUOUS. The reason is `No unique...` whenever binding count is not exactly one. Same source lines. |",
            "",
            f"In `semantic_gapfilled` output, **{len(no_unique)} mappings** have the `No unique semantic finding` "
            "reason. Split by recorded verdict:",
            "",
            "| Semantic verdict | Count | Expected IDs |",
            "|---|---:|---|",
        ]
    )
    no_unique_by_prediction: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in no_unique:
        no_unique_by_prediction[row["prediction"]].append(row)
    for verdict in ("FDO", "NOT_FDO", "AMBIGUOUS"):
        rows = no_unique_by_prediction.get(verdict, [])
        lines.append(
            f"| {verdict} | {len(rows)} | "
            f"{esc(', '.join(sorted(row['expected_id'] for row in rows)) or '—')} |"
        )
    lines.extend(
        [
            "",
            "A `No unique...` FDO is not a zero-binding FDO: the harness's empty verdict set maps to AMBIGUOUS. "
            "For a recorded FDO with that reason, the code implies multiple findings whose distinct verdict set "
            "was exactly `{FDO}`. This follows from the independent tests of verdict-set size and finding-list size. "
            "That same-verdict aggregation is explicit implementation behavior, not evidence of a single unique "
            "semantic explanation; the diagnostic reason is misleadingly phrased for it. Whether returning FDO "
            "for unanimous multiple findings is intended cannot be established from code alone. If the design "
            "contract requires a unique binding, this is a confirmed aggregation defect; if the contract permits "
            "unanimous aggregation, the defect is the reason text/traceability. No policy intent is assumed here.",
            "",
            "The ontology service deduplicates exact semantic rows and groups multiple purposes for identical "
            "data relationships before returning them "
            "[db_semantic_result_service.py:16-72](../../../Backend/app/ontology/db_semantic_result_service.py#L16-L72); "
            "the detector yields each remaining SPARQL binding "
            "[fuseki_semantic_detector.py:20-43](../../../Backend/app/ontology/fuseki_semantic_detector.py#L20-L43). "
            "`DBSemanticResultService.analyze` clears and rebuilds the graph, filters findings for the target app "
            "and `is_semantic_finding_usable`, then adapts each usable finding; it returns only findings that "
            "survive those filters and does not create a row for an unmatched expected mapping "
            "[db_semantic_result_service.py:177-252](../../../Backend/app/ontology/db_semantic_result_service.py#L177-L252).",
        ]
    )

    placeholder_markers = re.compile(
        r"NOT_CAPTURED|PENDING_CAPTURE|PENDING_REGION_CHECK|"
        r"PENDING_DIRECT_CAPTURE|policy text (?:is )?not captured|pending capture|"
        r"capture required|capture pending",
        re.IGNORECASE,
    )
    policy_rows: list[tuple[str, dict[str, Any]]] = []
    for app_id, policy in sorted(apps.items()):
        raw_text = str(policy["raw_text"] or "")
        if placeholder_markers.search(raw_text):
            state = "placeholder — explicit uncaptured/pending marker"
        elif "|" in raw_text:
            state = "placeholder/reference status note — not policy body"
        else:
            state = "not classifiable as policy body from stored text alone"
        policy_rows.append((app_id, policy | {"raw_text": raw_text, "text_state": state}))
    explicit_placeholder_count = sum(
        "explicit uncaptured/pending marker" in policy["text_state"]
        for _, policy in policy_rows
    )
    reference_note_count = sum(
        "reference status note" in policy["text_state"]
        for _, policy in policy_rows
    )
    body_count = len(policy_rows) - explicit_placeholder_count - reference_note_count

    lines.extend(
        [
            "",
            "## 6. Benchmark policy text and stored URL",
            "",
            f"All **{len(policy_rows)} canonical benchmark policy records** use `POL-<App ID>`. Text classification "
            "uses the stored text itself: explicit uncaptured/pending markers mean placeholder; a short value "
            "containing pipe-delimited source/status/notes is a reference/registry note, not a policy body. No "
            "record is called an actual captured policy body based only on title/status metadata. Length is Python "
            "character count; excerpt is at most 200 characters. The URL column reports `source_identifier` "
            "verbatim (not fetched); values without an `http(s)://` prefix are source descriptions, not URLs.",
            f"Classification totals: **{explicit_placeholder_count}** explicit uncaptured/pending placeholders, "
            f"**{reference_note_count}** registry/reference-status notes, and **{body_count}** records whose "
            "stored text is identifiable as an actual policy body.",
            "",
            "| App (ID) | Policy ID | Text classification | Length | Stored URL/source_identifier | Excerpt (max 200 chars) |",
            "|---|---|---|---:|---|---|",
        ]
    )
    for app_id, policy in policy_rows:
        excerpt = policy["raw_text"][:200]
        source_identifier = str(policy["source_identifier"] or "")
        if not source_identifier:
            source_kind = "NULL"
        elif source_identifier.lower().startswith(("http://", "https://")):
            source_kind = "URL"
        else:
            source_kind = "non-URL source descriptor"
        lines.append(
            f"| {esc(policy['application'])} ({app_id}) | {policy['policy_id']} | {policy['text_state']} | "
            f"{len(policy['raw_text'])} | {source_kind}: `{esc(source_identifier or '<NULL>')}` | "
            f"`{esc(excerpt)}` |"
        )

    lines.extend(
        [
            "",
            "## Confirmed defects vs design choices vs data gaps",
            "",
            "### Confirmed implementation inconsistencies (observable; intent caveated)",
            "",
            "- The comparator maps unclassifiable purpose text to `INCOMPATIBLE`; five Rule-4 cases have "
            "unclassified expected purpose and one hits the localization/security taxonomy collision. The decision "
            "engine then emits FDO. This path is confirmed; whether unknown purpose should be FDO or AMBIGUOUS "
            "requires a decision contract. "
            "[comparison_service.py:343-360](../../../Backend/app/services/comparison_service.py#L343-L360).",
            "- The evaluator labels every zero-or-many binding case `No unique...`; for multiple same-verdict "
            "findings it can report FDO while describing the finding as non-unique. This is a confirmed reason/"
            "traceability inconsistency. Whether same-verdict aggregation itself violates the intended contract is "
            "unresolved without a stated contract. "
            "[run_idf_b_eval.py:326-336](../../../Backend/eval/run_idf_b_eval.py#L326-L336).",
            "",
            "### Design choices",
            "",
            "- Evidence selection is exact type equality and selects a best purpose match only among same-type "
            "evidence; this makes relational Rule 5 unreachable. The latter is a confirmed code-path property, "
            "but whether it is a defect or intended selection boundary depends on whether unrelated evidence is "
            "supposed to reach Rule 5. "
            "[evidence_matcher.py:54-116](../../../Backend/app/services/evidence_matcher.py#L54-L116), "
            "[analysis_runner.py:150-183](../../../Backend/app/services/analysis_runner.py#L150-L183), "
            "[fdo_decision_service.py:119-136](../../../Backend/app/services/fdo_decision_service.py#L119-L136).",
            "- The semantic query is a positive mismatch/purpose-difference detector, not a complete per-mapping "
            "classifier; the eval harness assigns AMBIGUOUS to absent findings and aggregates unanimous verdicts "
            "[fdo_detection_queries.py:10-36](../../../Backend/app/ontology/fdo_detection_queries.py#L10-L36), "
            "[run_idf_b_eval.py:326-336](../../../Backend/eval/run_idf_b_eval.py#L326-L336).",
            "- `DATA.COMM.` → `DATA.COM.` is only a diagnostic alias hypothesis in this report. No rule or stored "
            "type was changed.",
            "",
            "### Data gaps",
            "",
            "- Stage 3 policy bodies are not independently verified against live URLs; all recorded URLs were read "
            "from SQLite and not fetched. Evidence is at "
            "[report.md:279-315](report.md#L279-L315).",
            "- Whether a repeated unanimous semantic verdict is intended to count as sufficiently unique cannot be "
            "settled without a product/design contract; observed behavior is "
            "[run_idf_b_eval.py:326-336](../../../Backend/eval/run_idf_b_eval.py#L326-L336).",
            "- Whether type namespace aliases such as `COMM` and `COM` are semantically equivalent cannot be "
            "settled from code alone; observed values are listed at "
            "[report.md:5-172](report.md#L5-L172).",
            "- Purpose-category labels are a code taxonomy, not human adjudications. A category mismatch can be a "
            "taxonomy limitation or an actual purpose mismatch; the rows are at "
            "[report.md:230-244](report.md#L230-L244), and the taxonomy is "
            "[comparison_service.py:3-98](../../../Backend/app/services/comparison_service.py#L3-L98).",
        ]
    )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        f"report={OUTPUT}\n"
        f"expected_sheet_types={len(workbook_types)}\n"
        f"database_expected_types={len(expected_db_types)}\n"
        f"policy_evidence_types={len(all_evidence_type_rows)}\n"
        f"rule1_with_app_evidence={len(rule1_rows)}\n"
        f"rule1_normalized_matches={alias_match_count}\n"
        f"rule1_no_normalized_type_match={no_related_count}\n"
        f"first_run_fdo={len(rule4_rows)}\n"
        f"semantic_no_unique={len(no_unique)}\n"
        f"policy_records={len(policy_rows)}"
    )


if __name__ == "__main__":
    main()
