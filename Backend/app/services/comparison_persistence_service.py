from sqlalchemy.orm import Session

from app.models.comparison import Comparison


def save_comparison(
    session: Session,
    comparison_id: str,
    analysis_id: str,
    expected_id: str,
    evidence_id: str | None,
    comparison,
) -> Comparison:
    existing = session.get(
        Comparison,
        comparison_id,
    )

    if existing:
        return existing

    record = Comparison(
        comparison_id=comparison_id,
        analysis_id=analysis_id,
        expected_id=expected_id,
        evidence_id=evidence_id,
        data_match=comparison.data_match,
        data_match_relation=comparison.data_match_relation,
        purpose_compatibility=comparison.purpose_compatibility,
        functional_relationship=comparison.functional_relationship,
        functional_justification=(
            comparison.functional_justification
        ),
        evidence_status=comparison.evidence_status,
    )

    session.add(record)
    session.flush()

    return record