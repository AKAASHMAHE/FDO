from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class OverreachCandidate(Base):
    __tablename__ = "overreach_candidates"

    candidate_id: Mapped[str] = mapped_column(
        String(255),
        primary_key=True,
    )

    analysis_id: Mapped[str] = mapped_column(
        ForeignKey("analyses.analysis_id"),
        nullable=False,
    )

    application_id: Mapped[str] = mapped_column(
        ForeignKey("applications.application_id"),
        nullable=False,
    )

    evidence_id: Mapped[str] = mapped_column(
        ForeignKey("policy_evidence.evidence_id"),
        nullable=False,
    )

    data_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    data_match: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    data_match_relation: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    purpose_compatibility: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    functional_relationship: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    evidence_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    fdo_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    decision_reason: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    decision_confidence: Mapped[float | None] = mapped_column(
        nullable=True,
    )
