from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Comparison(Base):
    __tablename__ = "comparisons"

    comparison_id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
    )

    analysis_id: Mapped[str] = mapped_column(
        ForeignKey("analyses.analysis_id"),
        nullable=False,
    )

    expected_id: Mapped[str] = mapped_column(
        ForeignKey("expected_mappings.expected_id"),
        nullable=False,
    )

    evidence_id: Mapped[str | None] = mapped_column(
        ForeignKey("policy_evidence.evidence_id"),
        nullable=True,
    )

    data_match: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    data_match_relation: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="NONE",
    )

    purpose_compatibility: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    functional_relationship: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    functional_justification: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    evidence_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
