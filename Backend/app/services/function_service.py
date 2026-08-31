from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.function import Function


def get_all_functions(session: Session) -> list[Function]:
    statement = select(Function).order_by(
        Function.application_id,
        Function.function_id,
    )

    return list(session.scalars(statement).all())


def get_functions_by_application(
    session: Session,
    application_id: str,
) -> list[Function]:
    statement = (
        select(Function)
        .where(Function.application_id == application_id)
        .order_by(Function.function_id)
    )

    return list(session.scalars(statement).all())


def get_function(
    session: Session,
    function_record_id: str,
) -> Function | None:
    return session.get(Function, function_record_id)