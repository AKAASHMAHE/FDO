from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class PolicyEvidence(Base):
    __tablename__ = "policy_evidence"

    evidence_id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
    )

    policy_id: Mapped[str] = mapped_column(
        ForeignKey("policy_documents.policy_id"),
        nullable=False,
    )

    data_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    purpose: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    entity: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    sharing: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    retention: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    evidence_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    source_section: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    extraction_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    confidence: Mapped[float | None] = mapped_column(
        nullable=True,
    )