from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class ExpectedMapping(Base):
    __tablename__ = "expected_mappings"

    expected_id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
    )

    application_id: Mapped[str] = mapped_column(
        ForeignKey("applications.application_id"),
        nullable=False,
    )

    function_id: Mapped[str] = mapped_column(
        ForeignKey("functions.function_id"),
        nullable=False,
    )

    data_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    necessity: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    expected_purpose: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    source_version: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )