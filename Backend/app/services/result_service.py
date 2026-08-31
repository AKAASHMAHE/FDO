from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.fdo_result import FDOResult


def save_fdo_result(
    session: Session,
    comparison_id: str,
    decision,
) -> FDOResult:
    result_id = f"RESULT-{comparison_id}"

    existing = session.get(
        FDOResult,
        result_id,
    )

    if existing:
        return existing

    result = FDOResult(
        result_id=result_id,
        comparison_id=comparison_id,
        fdo_status=decision.fdo_status,
        decision_reason=decision.decision_reason,
        decision_confidence=decision.decision_confidence,
        created_at=datetime.now(
            timezone.utc
        ).isoformat(),
    )

    session.add(result)
    session.flush()

    return result