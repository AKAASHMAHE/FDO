from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.application import Application
from app.models.policy_document import PolicyDocument
from app.models.policy_evidence import PolicyEvidence


def get_all_applications(session: Session) -> list[Application]:
    statement = select(Application).order_by(
        Application.application_id
    )

    return list(session.scalars(statement).all())


def get_application(
    session: Session,
    application_id: str,
) -> Application | None:
    return session.get(Application, application_id)


def get_application_readiness(
    session: Session,
    application_id: str,
):
    application = get_application(
        session,
        application_id,
    )

    if application is None:
        return None

    policy_statement = select(PolicyDocument).where(
        PolicyDocument.application_id
        == application_id
    )

    policies = list(
        session.scalars(policy_statement).all()
    )

    policy_ids = [
        policy.policy_id
        for policy in policies
    ]

    evidence_count = 0

    if policy_ids:
        evidence_statement = select(
            PolicyEvidence
        ).where(
            PolicyEvidence.policy_id.in_(policy_ids)
        )

        evidence_count = len(
            session.scalars(
                evidence_statement
            ).all()
        )

    return {
        "application_id": application.application_id,
        "application_name": application.application_name,
        "category": application.category,
        "policy_count": len(policies),
        "evidence_count": evidence_count,
        "ready_for_analysis": evidence_count > 0,
    }
def find_application_by_name_and_category(
    session: Session,
    application_name: str,
    category: str,
) -> Application | None:
    statement = (
        select(Application)
        .where(
            Application.application_name == application_name,
            Application.category == category,
        )
    )

    return session.scalars(statement).first()