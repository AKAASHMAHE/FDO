from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.policy_evidence import PolicyEvidence
from app.models.function import Function
from app.services.data_type_hierarchy import data_type_relation
from app.services.comparison_service import (
    classify_purpose_compatibility,
    normalize_purpose,
)


@dataclass
class EvidenceMatch:
    evidence: PolicyEvidence | None
    status: str
    reason: str
    data_match_relation: str | None = None


def _text_contains_function_context(
    evidence: PolicyEvidence,
    function: Function | None,
) -> bool:
    if function is None:
        return False

    haystack = normalize_purpose(
        " ".join(
            value
            for value in (
                evidence.purpose,
                evidence.entity,
                evidence.evidence_text,
            )
            if value
        )
    )

    needles = [
        function.function_name,
        function.function_id,
        function.feature,
        function.description,
    ]

    return any(
        normalize_purpose(value) in haystack
        for value in needles
        if value and normalize_purpose(value)
    )


def score_evidence_candidate(
    relation: str,
    purpose_result: str,
    extraction_status: str | None,
    confidence: float | None,
    function_related: bool,
) -> float:
    score = 10.0
    if relation == "EXACT":
        score += 15
    if purpose_result == "COMPATIBLE":
        score += 60
    elif purpose_result == "UNKNOWN":
        score += 10
    if function_related:
        score += 25
    if (extraction_status or "").strip().upper() == "EXTRACTED":
        score += 5
    score += min(confidence or 0.0, 1.0)
    return score


def find_best_matching_evidence(
    session: Session,
    policy_id: str,
    expected,
) -> EvidenceMatch:
    policy_evidence_rows = list(
        session.scalars(
            select(PolicyEvidence)
            .where(
                PolicyEvidence.policy_id == policy_id,
            )
            .order_by(PolicyEvidence.evidence_id)
        )
    )
    evidence_rows = [
        (evidence, data_type_relation(
            expected.data_type,
            evidence.data_type,
        ))
        for evidence in policy_evidence_rows
    ]
    evidence_rows = [
        (evidence, relation)
        for evidence, relation in evidence_rows
        if relation is not None
    ]

    if not evidence_rows:
        return EvidenceMatch(
            evidence=None,
            status="NO_EVIDENCE",
            reason="No policy evidence matched the expected data type.",
        )

    function = session.get(
        Function,
        expected.function_record_id,
    )

    scored = []

    for evidence, relation in evidence_rows:
        purpose_result = classify_purpose_compatibility(
            expected.expected_purpose,
            evidence.purpose,
        )
        function_related = _text_contains_function_context(
            evidence,
            function,
        )
        score = score_evidence_candidate(
            relation,
            purpose_result,
            evidence.extraction_status,
            evidence.confidence,
            function_related,
        )

        scored.append(
            (
                score,
                purpose_result,
                function_related,
                evidence,
                relation,
            )
        )

    scored.sort(
        key=lambda item: (
            item[0],
            item[1] == "COMPATIBLE",
            item[2],
        ),
        reverse=True,
    )

    best_score = scored[0][0]
    best = [
        item
        for item in scored
        if abs(item[0] - best_score) < 0.000001
    ]

    if len(best) > 1:
        return EvidenceMatch(
            evidence=None,
            status="AMBIGUOUS",
            reason=(
                "Multiple policy evidence rows matched equally well; "
                "the comparison remains ambiguous."
            ),
        )

    _, purpose_result, _, evidence, relation = best[0]

    if purpose_result == "INCOMPATIBLE" and len(evidence_rows) > 1:
        return EvidenceMatch(
            evidence=None,
            status="AMBIGUOUS",
            reason=(
                "Policy evidence matched the data type, but no unique "
                "purpose-compatible evidence could be selected."
            ),
        )

    return EvidenceMatch(
        evidence=evidence,
        status="MATCHED",
        reason="Selected the most purpose-compatible policy evidence.",
        data_match_relation=relation,
    )


def find_matching_evidence(
    session: Session,
    policy_id: str,
    expected_data_type: str,
) -> PolicyEvidence | None:
    """
    Find declared evidence for an expected data type
    within the specified policy.

    Multiple expected mappings may legitimately use
    the same evidence record.

    Returns:
        Matching PolicyEvidence, or None.
    """

    evidence_rows = session.scalars(
        select(PolicyEvidence)
        .where(PolicyEvidence.policy_id == policy_id)
        .order_by(PolicyEvidence.evidence_id)
    )
    return next(
        (
            evidence
            for evidence in evidence_rows
            if data_type_relation(
                expected_data_type,
                evidence.data_type,
            )
        ),
        None,
    )
