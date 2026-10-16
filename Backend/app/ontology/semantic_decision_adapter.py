"""Adapt semantic query bindings to relational decision semantics."""

from app.services.comparison_service import (
    classify_purpose_compatibility,
    normalize_purpose,
)
from app.services.data_type_hierarchy import data_type_relation
from app.services.ancillary_baseline import is_ancillary_declaration
from app.services.evidence_matcher import score_evidence_candidate
from app.services.fdo_decision_service import (
    FDODecisionInput,
    FDODecisionOutput,
    evaluate_fdo_decision,
)


def _decision_for_finding(finding: dict) -> FDODecisionOutput:
    expected_type = finding.get("expected_type")
    declared_type = finding.get("declared_type")
    relation = finding.get("type_relation")
    if relation not in {
        "EXACT",
        "BROADER_EVIDENCE",
        "NARROWER_EVIDENCE",
    }:
        relation = data_type_relation(
        str(expected_type or ""),
        str(declared_type) if declared_type is not None else None,
        )
    declared_id = finding.get("declared_id") or finding.get("declared_data")
    data_match = (
        "NO_EVIDENCE"
        if not declared_type
        else "EXACT_MATCH"
        if relation == "EXACT"
        else "HIERARCHICAL_MATCH"
        if relation
        else "NO_MATCH"
    )
    declared_id = finding.get("declared_id") or finding.get("declared_data")
    extraction_status = str(
        finding.get("extraction_status")
        or ("EXTRACTED" if declared_type else "NO_EVIDENCE")
    ).strip().upper()

    decision = evaluate_fdo_decision(
        FDODecisionInput(
            expected_id=str(finding.get("expected_id") or ""),
            application_id=str(finding.get("application_id") or "semantic"),
            expected_data_type=str(expected_type or ""),
            expected_necessity=str(
                finding.get("expected_necessity") or "UNKNOWN"
            ),
            expected_purpose=str(finding.get("expected_purpose") or ""),
            declared_evidence_id=declared_id,
            declared_data_type=(
                str(declared_type)
                if declared_type is not None
                else None
            ),
            declared_purpose=finding.get("declared_purpose"),
            data_match=data_match,
            purpose_compatibility=classify_purpose_compatibility(
                finding.get("expected_purpose"),
                finding.get("declared_purpose"),
            ),
            functional_relationship=(
                "RELATED" if declared_id else "NO_EVIDENCE"
            ),
            evidence_status=extraction_status,
            data_match_relation=relation or "NONE",
        )
    )
    return decision


def semantic_finding_to_decision_input(
    finding: dict,
) -> FDODecisionInput:
    """Convert a covered semantic row into the common decision input."""
    expected_type = finding.get("expected_type")
    declared_type = finding.get("declared_type")
    relation = finding.get("type_relation")
    if relation not in {
        "EXACT",
        "BROADER_EVIDENCE",
        "NARROWER_EVIDENCE",
    }:
        relation = data_type_relation(
        str(expected_type or ""),
        str(declared_type) if declared_type is not None else None,
        )
    declared_id = finding.get("declared_id") or finding.get("declared_data")
    data_match = (
        "NO_EVIDENCE"
        if not declared_type
        else "EXACT_MATCH"
        if relation == "EXACT"
        else "HIERARCHICAL_MATCH"
        if relation
        else "NO_MATCH"
    )
    return FDODecisionInput(
        expected_id=str(finding.get("expected_id") or ""),
        application_id=str(finding.get("application_id") or "semantic"),
        expected_data_type=str(expected_type or ""),
        expected_necessity=str(
            finding.get("expected_necessity") or "UNKNOWN"
        ),
        expected_purpose=str(finding.get("expected_purpose") or ""),
        declared_evidence_id=declared_id,
        declared_data_type=(
            str(declared_type) if declared_type is not None else None
        ),
        declared_purpose=finding.get("declared_purpose"),
        data_match=data_match,
        purpose_compatibility=classify_purpose_compatibility(
            finding.get("expected_purpose"),
            finding.get("declared_purpose"),
        ),
        functional_relationship=(
            "RELATED" if declared_id else "NO_EVIDENCE"
        ),
        evidence_status=str(
            finding.get("extraction_status")
            or ("EXTRACTED" if declared_type else "NO_EVIDENCE")
        ).strip().upper(),
        data_match_relation=relation or "NONE",
    )


def decide_semantic_finding(
    finding: dict,
) -> FDODecisionOutput:
    decision = _decision_for_finding(finding)
    _append_relation_reason(decision)
    return decision


def _append_relation_reason(decision: FDODecisionOutput) -> None:
    direction = {
        "EXACT": "exact",
        "BROADER_EVIDENCE": "broader",
        "NARROWER_EVIDENCE": "narrower",
    }.get(decision.data_match_relation)
    if (
        direction
        and f"matched via {direction} type" not in decision.decision_reason.lower()
    ):
        decision.decision_reason = (
            f"{decision.decision_reason} Matched via {direction} type."
        )


def _function_related(row: dict) -> bool:
    evidence_context = normalize_purpose(
        " ".join(
            str(row.get(key) or "")
            for key in ("declared_purpose", "entity", "evidence_text")
        )
    )
    needles = (
        row.get("function_name"),
        row.get("function_id"),
    )
    return any(
        normalize_purpose(str(needle)) in evidence_context
        for needle in needles
        if needle and normalize_purpose(str(needle))
    )


def _rank_covered(expected_purpose: str, rows: list[dict]) -> list[tuple[float, dict]]:
    ranked = []
    for row in rows:
        relation = str(row.get("type_relation") or "EXACT")
        purpose_result = classify_purpose_compatibility(
            expected_purpose,
            row.get("declared_purpose"),
        )
        confidence_value = row.get("confidence")
        try:
            confidence = float(confidence_value or 0.0)
        except (TypeError, ValueError):
            confidence = 0.0
        ranked.append(
            (
                score_evidence_candidate(
                    relation,
                    purpose_result,
                    row.get("extraction_status"),
                    confidence,
                    _function_related(row),
                ),
                row,
            )
        )
    return sorted(
        ranked,
        key=lambda scored: (
            scored[0],
            classify_purpose_compatibility(
                expected_purpose,
                scored[1].get("declared_purpose"),
            ) == "COMPATIBLE",
            _function_related(scored[1]),
        ),
        reverse=True,
    )


def adapt_semantic_results(
    application_id: str,
    application_uri: str,
    expected_mappings: list,
    covered_rows: list[dict],
    uncovered_rows: list[dict],
) -> list[dict]:
    """Return one chosen semantic decision per expected mapping plus uncovered declarations."""
    rows_by_expected: dict[str, list[dict]] = {}
    for row in covered_rows:
        if str(row.get("application_id") or "") != application_id:
            continue
        rows_by_expected.setdefault(
            str(row.get("expected_id") or ""),
            [],
        ).append(row)

    results = []
    for expected in expected_mappings:
        candidates = _rank_covered(
            expected.expected_purpose,
            rows_by_expected.get(expected.expected_id, []),
        )
        if not candidates:
            decision = evaluate_fdo_decision(
                FDODecisionInput(
                    expected_id=expected.expected_id,
                    application_id=application_id,
                    expected_data_type=expected.data_type,
                    expected_necessity=expected.necessity,
                    expected_purpose=expected.expected_purpose,
                    declared_evidence_id=None,
                    declared_data_type=None,
                    declared_purpose=None,
                    data_match="NO_EVIDENCE",
                    purpose_compatibility="UNKNOWN",
                    functional_relationship="NO_EVIDENCE",
                    evidence_status="NO_EVIDENCE",
                )
            )
            results.append(
                _semantic_result(
                    application_id,
                    application_uri,
                    expected.expected_id,
                    "",
                    expected.data_type,
                    "",
                    expected.expected_purpose,
                    "",
                    "NONE",
                    decision,
                    "No semantic finding was returned for this expected mapping.",
                    str(getattr(expected, "function_record_id", "") or ""),
                    "NO_EVIDENCE",
                )
            )
            continue

        best_score, selected = candidates[0]
        equally_ranked = [
            row for score, row in candidates
            if abs(score - best_score) < 0.000001
        ]
        relation = str(selected.get("type_relation") or "EXACT")
        if (
            len(equally_ranked) > 1
            or (
                classify_purpose_compatibility(
                    expected.expected_purpose,
                    selected.get("declared_purpose"),
                ) == "INCOMPATIBLE"
                and len(candidates) > 1
            )
        ):
            decision = FDODecisionOutput(
                "AMBIGUOUS",
                "Several covered declarations were equally suitable; "
                "no unique declaration could be selected.",
                0.40,
            )
        else:
            decision = _decision_for_finding(
                {
                    **selected,
                    "expected_id": expected.expected_id,
                    "application_id": application_id,
                    "expected_type": expected.data_type,
                    "expected_purpose": expected.expected_purpose,
                    "expected_necessity": expected.necessity,
                }
            )
        decision.data_match_relation = relation
        _append_relation_reason(decision)
        count_reason = (
            "One covered declaration was evaluated."
            if len(candidates) == 1
            else f"Several ({len(candidates)}) covered declarations were ranked; "
            "only the best-ranked declaration was evaluated."
        )
        results.append(
            _semantic_result(
                application_id,
                application_uri,
                expected.expected_id,
                str(selected.get("declared_id") or ""),
                expected.data_type,
                str(selected.get("declared_type") or ""),
                expected.expected_purpose,
                str(selected.get("declared_purpose") or ""),
                relation,
                decision,
                count_reason,
                str(
                    selected.get("function_name")
                    or selected.get("function_id")
                    or selected.get("function")
                    or ""
                ),
                "EXACT_MATCH" if relation == "EXACT" else "HIERARCHICAL_MATCH",
            )
        )

    for row in uncovered_rows:
        if str(row.get("application_id") or "") != application_id:
            continue
        declared_type = str(row.get("declared_type") or "")
        declared_purpose = str(row.get("declared_purpose") or "")
        declared_id = str(row.get("declared_id") or "")
        evidence_status = str(
            row.get("extraction_status") or "UNKNOWN"
        ).strip().upper()
        purposes = [
            classify_purpose_compatibility(
                item.expected_purpose,
                declared_purpose,
            )
            for item in expected_mappings
        ]
        purpose_result = (
            "COMPATIBLE"
            if "COMPATIBLE" in purposes
            else "UNKNOWN"
            if "UNKNOWN" in purposes or not purposes
            else "INCOMPATIBLE"
        )
        if is_ancillary_declaration(declared_type, declared_purpose):
            decision = evaluate_fdo_decision(
                FDODecisionInput(
                    expected_id=f"OVERREACH:{declared_id}",
                    application_id=application_id,
                    expected_data_type="",
                    expected_necessity="UNKNOWN",
                    expected_purpose="",
                    declared_evidence_id=declared_id or None,
                    declared_data_type=declared_type,
                    declared_purpose=declared_purpose,
                    data_match="ANCILLARY",
                    purpose_compatibility="ANCILLARY",
                    functional_relationship="RELATED",
                    evidence_status=evidence_status,
                    is_uncovered_declaration=True,
                )
            )
            data_match = "ANCILLARY"
        else:
            decision = evaluate_fdo_decision(
                FDODecisionInput(
                    expected_id=f"OVERREACH:{declared_id}",
                    application_id=application_id,
                    expected_data_type="",
                    expected_necessity="UNKNOWN",
                    expected_purpose="",
                    declared_evidence_id=declared_id or None,
                    declared_data_type=declared_type,
                    declared_purpose=declared_purpose,
                    data_match="NO_MATCH",
                    purpose_compatibility=purpose_result,
                    functional_relationship="RELATED",
                    evidence_status=evidence_status,
                    is_uncovered_declaration=True,
                )
            )
            data_match = "NO_MATCH"
        results.append(
            _semantic_result(
                application_id,
                application_uri,
                f"OVERREACH:{declared_id}",
                declared_id,
                "",
                declared_type,
                "",
                declared_purpose,
                "NONE",
                decision,
                decision.decision_reason,
                "",
                data_match,
            )
        )
    return results


def _semantic_result(
    application_id: str,
    application_uri: str,
    expected_id: str,
    declared_id: str,
    expected_type: str,
    declared_type: str,
    expected_purpose: str,
    declared_purpose: str,
    relation: str,
    decision: FDODecisionOutput,
    reason: str,
    function: str,
    data_match: str = "NONE",
) -> dict:
    return {
        "application_id": application_id,
        "application": application_uri,
        "function": function,
        "expected_data": expected_id,
        "declared_data": declared_id,
        "expected_type": expected_type,
        "declared_type": declared_type,
        "expected_purpose": expected_purpose,
        "declared_purpose": declared_purpose,
        "data_match_relation": relation,
        "data_match": data_match,
        "fdo_status": decision.fdo_status,
        "confidence": decision.decision_confidence,
        "reason": f"{decision.decision_reason} {reason}".strip(),
    }
