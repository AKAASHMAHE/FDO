from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.analysis import Analysis
from app.models.comparison import Comparison
from app.models.fdo_result import FDOResult
from app.models.application import Application

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


def get_all_analyses(session: Session):
    statement = (
        select(Analysis, Application)
        .join(
            Application,
            Analysis.application_id == Application.application_id,
        )
        .order_by(Analysis.created_at.desc())
    )

    rows = session.execute(statement).all()

    return [
        {
            "analysis_id": analysis.analysis_id,
            "application_id": analysis.application_id,
            "application_name": application.application_name,
            "category": application.category,
            "policy_id": analysis.policy_id,
            "analysis_status": analysis.analysis_status,
            "total_mappings": analysis.total_mappings,
            "fdo_count": analysis.fdo_count,
            "not_fdo_count": analysis.not_fdo_count,
            "ambiguous_count": analysis.ambiguous_count,
            "created_at": analysis.created_at,
        }
        for analysis, application in rows
    ]


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