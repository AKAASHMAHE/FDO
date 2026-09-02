from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.explanation import Explanation


def save_explanation(
    session: Session,
    result_id: str,
    decision,
    evidence_summary: str | None = None,
    limitations: str | None = None,
) -> Explanation:

    explanation_id = f"EXPLANATION-{result_id}"

    existing = session.get(
        Explanation,
        explanation_id,
    )

    if existing:
        return existing

    explanation = Explanation(
        explanation_id=explanation_id,
        result_id=result_id,
        explanation_text=decision.decision_reason,
        evidence_summary=evidence_summary,
        limitations=limitations,
        created_at=datetime.now(
            timezone.utc
        ).isoformat(),
    )

    session.add(explanation)
    session.flush()

    return explanation