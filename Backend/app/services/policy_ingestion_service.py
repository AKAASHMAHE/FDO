from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy.orm import Session

from app.models.policy_document import PolicyDocument
from app.models.policy_evidence import PolicyEvidence


def create_runtime_policy(
    session: Session,
    application_id: str,
    policy_text: str,
    policy_source: str | None,
    evidence: list[dict],
    analysis_id: str,
) -> PolicyDocument:
    """
    Create a runtime policy document and persist extracted evidence.

    Runtime AI analyses receive their own policy/evidence records so
    the Stage 3 benchmark data remains untouched.
    """

    policy_id = f"AI-POL-{analysis_id}"

    policy = PolicyDocument(
        policy_id=policy_id,
        application_id=application_id,
        source_type="RUNTIME_AI",
        source_identifier=policy_source,
        document_name=f"Runtime AI Policy - {analysis_id}",
        raw_text=policy_text,
        retrieved_at=datetime.now(timezone.utc).isoformat(),
        created_at=datetime.now(timezone.utc).isoformat(),
    )

    session.add(policy)
    session.flush()

    for item in evidence:
        evidence_id = item.get("evidence_id")

        if not evidence_id:
            evidence_id = f"AI-{uuid4().hex[:8]}"

        evidence_record = PolicyEvidence(
            evidence_id=evidence_id,
            policy_id=policy_id,
            data_type=item.get("data_type"),
            purpose=item.get("purpose"),
            entity=item.get("entity"),
            sharing=item.get("sharing"),
            retention=item.get("retention"),
            evidence_text=(
                item.get("evidence_text")
                or "No evidence text captured."
            ),
            source_section=item.get("source_section"),
            extraction_status=(
                item.get("extraction_status")
                or "UNKNOWN"
            ),
            confidence=item.get("confidence"),
        )

        session.add(evidence_record)

    session.flush()

    return policy