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
