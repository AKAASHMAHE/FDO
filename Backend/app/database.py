from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

from app.config import settings


engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def ensure_sqlite_schema_compatibility() -> None:
    from app import models
    from app.models.base import Base

    Base.metadata.create_all(
        bind=engine,
        tables=[models.OverreachCandidate.__table__],
    )

    if not settings.database_url.startswith("sqlite"):
        return

    with engine.begin() as connection:
        rows = connection.execute(
            text("PRAGMA table_info(expected_mappings)")
        ).fetchall()

        column_names = {
            row[1]
            for row in rows
        }

        if (
            rows
            and "baseline_justification" not in column_names
        ):
            connection.execute(
                text(
                    "ALTER TABLE expected_mappings "
                    "ADD COLUMN baseline_justification TEXT"
                )
            )

        comparison_rows = connection.execute(
            text("PRAGMA table_info(comparisons)")
        ).fetchall()
        comparison_columns = {
            row[1]
            for row in comparison_rows
        }
        if (
            comparison_rows
            and "data_match_relation" not in comparison_columns
        ):
            connection.execute(
                text(
                    "ALTER TABLE comparisons "
                    "ADD COLUMN data_match_relation "
                    "VARCHAR(50) NOT NULL DEFAULT 'NONE'"
                )
            )

        semantic_rows = connection.execute(
            text("PRAGMA table_info(semantic_fdo_results)")
        ).fetchall()
        semantic_columns = {
            row[1]
            for row in semantic_rows
        }
        if (
            semantic_rows
            and "data_match_relation" not in semantic_columns
        ):
            connection.execute(
                text(
                    "ALTER TABLE semantic_fdo_results "
                    "ADD COLUMN data_match_relation "
                    "VARCHAR(50) NOT NULL DEFAULT 'NONE'"
                )
            )

        explanation_rows = connection.execute(
            text("PRAGMA table_info(explanations)")
        ).fetchall()
        explanation_columns = {
            row[1]
            for row in explanation_rows
        }
        if (
            explanation_rows
            and "data_match_relation" not in explanation_columns
        ):
            connection.execute(
                text(
                    "ALTER TABLE explanations "
                    "ADD COLUMN data_match_relation "
                    "VARCHAR(50) NOT NULL DEFAULT 'NONE'"
                )
            )
