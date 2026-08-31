from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.expected_mapping import ExpectedMapping


def get_all_expected_mappings(
    session: Session,
) -> list[ExpectedMapping]:
    statement = select(ExpectedMapping).order_by(
        ExpectedMapping.application_id,
        ExpectedMapping.expected_id,
    )

    return list(session.scalars(statement).all())


def get_expected_mappings_by_application(
    session: Session,
    application_id: str,
) -> list[ExpectedMapping]:
    statement = (
        select(ExpectedMapping)
        .where(
            ExpectedMapping.application_id == application_id
        )
        .order_by(ExpectedMapping.expected_id)
    )

    return list(session.scalars(statement).all())


def get_expected_mappings_by_function(
    session: Session,
    function_record_id: str,
) -> list[ExpectedMapping]:
    statement = (
        select(ExpectedMapping)
        .where(
            ExpectedMapping.function_record_id
            == function_record_id
        )
        .order_by(ExpectedMapping.expected_id)
    )

    return list(session.scalars(statement).all())


def get_expected_mapping(
    session: Session,
    expected_id: str,
) -> ExpectedMapping | None:
    return session.get(ExpectedMapping, expected_id)