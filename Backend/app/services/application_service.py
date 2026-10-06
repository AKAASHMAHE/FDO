import re

from sqlalchemy import func, select
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


def normalize_application_name(
    application_name: str,
) -> str:
    return " ".join(application_name.strip().lower().split())


def find_application_by_name(
    session: Session,
    application_name: str,
) -> Application | None:
    normalized_name = normalize_application_name(
        application_name
    )

    if not normalized_name:
        return None

    statement = select(Application).where(
        func.lower(func.trim(Application.application_name))
        == normalized_name
    )

    return session.scalars(statement).first()


def _application_id_base(application_name: str) -> str:
    normalized = normalize_application_name(
        application_name
    )
    slug = re.sub(r"[^a-z0-9]+", "-", normalized).strip("-")

    if not slug:
        slug = "application"

    return f"APP-{slug.upper()}"[:100]


def _generate_application_id(
    session: Session,
    application_name: str,
) -> str:
    base = _application_id_base(application_name)

    if session.get(Application, base) is None:
        return base

    suffix = 2

    while True:
        suffix_text = f"-{suffix}"
        candidate = (
            f"{base[:100 - len(suffix_text)]}{suffix_text}"
        )

        if session.get(Application, candidate) is None:
            return candidate

        suffix += 1


def get_or_create_application_for_analysis(
    session: Session,
    application_name: str,
    category: str,
    description: str | None = None,
) -> Application:
    application = find_application_by_name(
        session,
        application_name,
    )

    if application is not None:
        return application

    application = Application(
        application_id=_generate_application_id(
            session,
            application_name,
        ),
        application_name=application_name.strip(),
        category=category.strip(),
        description=description,
    )

    session.add(application)
    session.flush()

    return application


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
