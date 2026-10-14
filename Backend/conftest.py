import sqlite3
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture
def isolated_app_database(tmp_path, monkeypatch):
    source = Path(__file__).parent / "fdo_privacy.db"
    destination = tmp_path / "fdo_privacy_test.db"
    source_connection = sqlite3.connect(
        f"{source.resolve().as_uri()}?mode=ro",
        uri=True,
    )
    destination_connection = sqlite3.connect(destination)
    try:
        source_connection.backup(destination_connection)
    finally:
        destination_connection.close()
        source_connection.close()

    isolated_engine = create_engine(
        f"sqlite:///{destination}",
        connect_args={"check_same_thread": False},
    )
    isolated_session_local = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=isolated_engine,
    )

    from app import database, main

    monkeypatch.setattr(database, "engine", isolated_engine)
    monkeypatch.setattr(database, "SessionLocal", isolated_session_local)
    monkeypatch.setattr(main, "SessionLocal", isolated_session_local)

    try:
        yield isolated_engine, isolated_session_local
    finally:
        isolated_engine.dispose()
