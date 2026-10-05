from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class SemanticFDOResult(Base):
    __tablename__ = "semantic_fdo_results"

    semantic_result_id: Mapped[str] = mapped_column(
        String(100),
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

    application: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    function: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    expected_data: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    declared_data: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    expected_type: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    declared_type: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    expected_purpose: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    declared_purpose: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    fdo_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    confidence: Mapped[float | None] = mapped_column(
        nullable=True,
    )

    reason: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )