from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class FDOResult(Base):
    __tablename__ = "fdo_results"

    result_id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
    )

    comparison_id: Mapped[str] = mapped_column(
        ForeignKey("comparisons.comparison_id"),
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

    created_at: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )