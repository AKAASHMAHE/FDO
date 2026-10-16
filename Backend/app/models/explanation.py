from sqlalchemy import ForeignKey, Text, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Explanation(Base):
    __tablename__ = "explanations"

    explanation_id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
    )

    result_id: Mapped[str] = mapped_column(
        ForeignKey("fdo_results.result_id"),
        nullable=False,
    )

    explanation_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    data_match_relation: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="NONE",
    )

    evidence_summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    limitations: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )