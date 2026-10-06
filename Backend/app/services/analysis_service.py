from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.analysis import Analysis
from app.models.comparison import Comparison
from app.models.fdo_result import FDOResult


def create_analysis(
    session: Session,
    analysis_id: str,
    application_id: str,
    policy_id: str,
) -> Analysis:
    existing = session.get(
        Analysis,
        analysis_id,
    )

    if existing:
        return existing

    analysis = Analysis(
        analysis_id=analysis_id,
        application_id=application_id,
        policy_id=policy_id,
        analysis_status="CREATED",
        total_mappings=0,
        fdo_count=0,
        not_fdo_count=0,
        ambiguous_count=0,
        created_at=datetime.now(
            timezone.utc
        ).isoformat(),
    )

    session.add(analysis)
    session.flush()

    return analysis


def get_analysis(
    session: Session,
    analysis_id: str,
) -> Analysis | None:
    return session.get(
        Analysis,
        analysis_id,
    )


def get_all_analyses(
    session: Session,
) -> list[Analysis]:
    statement = (
        select(Analysis)
        .order_by(Analysis.created_at.desc())
    )

    return list(
        session.scalars(statement).all()
    )


def get_comparisons_by_analysis(
    session: Session,
    analysis_id: str,
) -> list[Comparison]:
    statement = (
        select(Comparison)
        .where(
            Comparison.analysis_id
            == analysis_id
        )
        .order_by(Comparison.expected_id)
    )

    return list(
        session.scalars(statement).all()
    )


def get_fdo_results_by_analysis(
    session: Session,
    analysis_id: str,
) -> list[FDOResult]:
    statement = (
        select(FDOResult)
        .join(
            Comparison,
            FDOResult.comparison_id
            == Comparison.comparison_id,
        )
        .where(
            Comparison.analysis_id
            == analysis_id
        )
        .order_by(Comparison.expected_id)
    )

    return list(
        session.scalars(statement).all()
    )