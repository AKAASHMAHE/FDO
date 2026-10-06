from app.database import engine, ensure_sqlite_schema_compatibility
from app.models.base import Base
from app import models


def init_db():
    Base.metadata.create_all(bind=engine)
    ensure_sqlite_schema_compatibility()


if __name__ == "__main__":
    init_db()
    print("Database tables created successfully.")
