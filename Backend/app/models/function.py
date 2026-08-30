from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Function(Base):
    __tablename__ = "functions"

    function_id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
    )

    application_id: Mapped[str] = mapped_column(
        ForeignKey("applications.application_id"),
        nullable=False,
    )

    function_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    feature: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )