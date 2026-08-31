from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.policy_document import PolicyDocument


def get_all_policy_documents(
    session: Session,
) -> list[PolicyDocument]:
    statement = select(PolicyDocument).order_by(
        PolicyDocument.policy_id
    )

    return list(session.scalars(statement).all())


def get_policy_documents_by_application(
    session: Session,
    application_id: str,
) -> list[PolicyDocument]:
    statement = (
        select(PolicyDocument)
        .where(
            PolicyDocument.application_id == application_id
        )
        .order_by(PolicyDocument.policy_id)
    )

    return list(session.scalars(statement).all())


def get_policy_document(
    session: Session,
    policy_id: str,
) -> PolicyDocument | None:
    return session.get(PolicyDocument, policy_id)