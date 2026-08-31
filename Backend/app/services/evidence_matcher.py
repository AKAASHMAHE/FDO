from sqlalchemy.orm import Session

from app.models.policy_evidence import PolicyEvidence


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

    evidence = (
        session.query(PolicyEvidence)
        .filter(
            PolicyEvidence.policy_id == policy_id,
            PolicyEvidence.data_type == expected_data_type,
        )
        .order_by(PolicyEvidence.evidence_id)
        .first()
    )

    return evidence