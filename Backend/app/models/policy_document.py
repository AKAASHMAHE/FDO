from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class PolicyDocument(Base):
    __tablename__ = "policy_documents"

    policy_id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
    )

    application_id: Mapped[str] = mapped_column(
        ForeignKey("applications.application_id"),
        nullable=False,
    )

    source_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    source_identifier: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    document_name: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    raw_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    retrieved_at: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    created_at: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )