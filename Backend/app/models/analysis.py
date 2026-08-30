from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Analysis(Base):
    __tablename__ = "analyses"

    analysis_id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
    )

    application_id: Mapped[str] = mapped_column(
        ForeignKey("applications.application_id"),
        nullable=False,
    )

    policy_id: Mapped[str] = mapped_column(
        ForeignKey("policy_documents.policy_id"),
        nullable=False,
    )

    analysis_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    total_mappings: Mapped[int] = mapped_column(
        nullable=False,
        default=0,
    )

    fdo_count: Mapped[int] = mapped_column(
        nullable=False,
        default=0,
    )

    not_fdo_count: Mapped[int] = mapped_column(
        nullable=False,
        default=0,
    )

    ambiguous_count: Mapped[int] = mapped_column(
        nullable=False,
        default=0,
    )

    created_at: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )