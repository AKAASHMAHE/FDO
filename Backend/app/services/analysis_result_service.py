from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.comparison import Comparison
from app.models.expected_mapping import ExpectedMapping
from app.models.fdo_result import FDOResult
from app.models.policy_evidence import PolicyEvidence
from app.models.explanation import Explanation


def get_analysis_results(
    session: Session,
    analysis_id: str,
) -> list[dict]:

    statement = (
        select(
            Comparison,
            ExpectedMapping,
            PolicyEvidence,
            FDOResult,
            Explanation,
        )
        .join(
            ExpectedMapping,
            ExpectedMapping.expected_id
            == Comparison.expected_id,
        )
        .outerjoin(
            PolicyEvidence,
            PolicyEvidence.evidence_id
            == Comparison.evidence_id,
        )
        .join(
            FDOResult,
            FDOResult.comparison_id
            == Comparison.comparison_id,
        )
        .outerjoin(
            Explanation,
            Explanation.result_id
            == FDOResult.result_id,
        )
        .where(
            Comparison.analysis_id
            == analysis_id
        )
        .order_by(
            Comparison.expected_id
        )
    )

    rows = session.execute(statement).all()

    results = []

    for (
        comparison,
        expected_mapping,
        evidence,
        fdo_result,
        explanation,
    ) in rows:

        results.append(
            {
                # Existing fields
                "expected_id": comparison.expected_id,
                "evidence_id": comparison.evidence_id,
                "data_match": comparison.data_match,
                "purpose_compatibility": (
                    comparison.purpose_compatibility
                ),
                "functional_relationship": (
                    comparison.functional_relationship
                ),
                "functional_justification": (
                    comparison.functional_justification
                ),
                "evidence_status": comparison.evidence_status,

                # FDO fields
                "fdo_status": fdo_result.fdo_status,
                "decision_reason": fdo_result.decision_reason,
                "decision_confidence": (
                    fdo_result.decision_confidence
                ),

                # Stage 8 richer fields
                "expected_necessity": (
                    expected_mapping.necessity
                ),
                "expected_purpose": (
                    expected_mapping.expected_purpose
                ),
                "declared_data_type": (
                    evidence.data_type
                    if evidence
                    else None
                ),
                "declared_purpose": (
                    evidence.purpose
                    if evidence
                    else None
                ),
                "explanation": (
                    explanation.explanation_text
                    if explanation
                    else None
                ),
                "evidence_available": (
                    evidence is not None
                ),
            }
        )

    return results