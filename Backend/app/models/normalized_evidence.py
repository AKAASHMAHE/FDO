from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class NormalizedEvidence(Base):
    __tablename__ = "normalized_evidence"

    normalized_id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
    )

    evidence_id: Mapped[str] = mapped_column(
        ForeignKey("policy_evidence.evidence_id"),
        nullable=False,
    )

    normalized_data_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    normalized_purpose: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    normalization_note: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    normalization_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )