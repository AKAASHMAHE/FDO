from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.policy_evidence import PolicyEvidence


def get_all_evidence(
    session: Session,
) -> list[PolicyEvidence]:
    statement = select(PolicyEvidence).order_by(
        PolicyEvidence.evidence_id
    )

    return list(session.scalars(statement).all())


def get_evidence_by_policy(
    session: Session,
    policy_id: str,
) -> list[PolicyEvidence]:
    statement = (
        select(PolicyEvidence)
        .where(
            PolicyEvidence.policy_id == policy_id
        )
        .order_by(PolicyEvidence.evidence_id)
    )

    return list(session.scalars(statement).all())


def get_evidence_by_data_type(
    session: Session,
    data_type: str,
) -> list[PolicyEvidence]:
    statement = (
        select(PolicyEvidence)
        .where(
            PolicyEvidence.data_type == data_type
        )
        .order_by(PolicyEvidence.evidence_id)
    )

    return list(session.scalars(statement).all())


def get_evidence(
    session: Session,
    evidence_id: str,
) -> PolicyEvidence | None:
    return session.get(PolicyEvidence, evidence_id)