from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.comparison import Comparison
from app.models.fdo_result import FDOResult


def get_analysis_results(
    session: Session,
    analysis_id: str,
) -> list[dict]:
    statement = (
        select(Comparison, FDOResult)
        .join(
            FDOResult,
            FDOResult.comparison_id
            == Comparison.comparison_id,
        )
        .where(
            Comparison.analysis_id
            == analysis_id
        )
        .order_by(Comparison.expected_id)
    )

    rows = session.execute(statement).all()

    results = []

    for comparison, fdo_result in rows:
        results.append(
            {
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
                "fdo_status": fdo_result.fdo_status,
                "decision_reason": fdo_result.decision_reason,
                "decision_confidence": (
                    fdo_result.decision_confidence
                ),
            }
        )

    return results