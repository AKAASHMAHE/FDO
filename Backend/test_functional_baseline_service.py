from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from app import models  # noqa: F401
from app.models.application import Application
from app.models.base import Base
from app.models.expected_mapping import ExpectedMapping
from app.models.function import Function
from app.services.functional_baseline_service import (
    BASELINE_AI_DERIVED,
    BASELINE_CURATED,
    ensure_functional_baseline,
)


def make_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )
    return SessionLocal()


def add_application(session):
    application = Application(
        application_id="APP-VIDEO-CHAT",
        application_name="Video Chat",
        category="Communication",
        description="Video calling and messaging",
    )
    session.add(application)
    session.flush()
    return application


def test_curated_baseline_is_used_without_ai(monkeypatch):
    session = make_session()
    application = add_application(session)
    function = Function(
        function_record_id="FUNC-1",
        function_id="FUNC.VIDEO",
        application_id=application.application_id,
        function_name="Video Call",
    )
    session.add(function)
    session.add(
        ExpectedMapping(
            expected_id="EXP-1",
            application_id=application.application_id,
            function_record_id=function.function_record_id,
            data_type="DATA.MEDIA",
            necessity="REQUIRED",
            expected_purpose="Enable video communication",
            source_version="CURATED",
        )
    )
    session.flush()

    def fail_if_called(**kwargs):
        raise AssertionError("AI baseline should not run")

    monkeypatch.setattr(
        "app.services.functional_baseline_service."
        "generate_functional_baseline_with_ai",
        fail_if_called,
    )

    result = ensure_functional_baseline(
        session,
        application,
    )

    assert result.source == BASELINE_CURATED
    assert result.available is True
    assert result.generated is False


def test_unknown_application_generates_ai_baseline(monkeypatch):
    session = make_session()
    application = add_application(session)
    seen = {}

    def fake_generator(**kwargs):
        seen.update(kwargs)
        return {
            "functions": [
                {
                    "function_name": "Video Call",
                    "description": "Live video calling",
                    "expected_data": [
                        {
                            "data_type": "DATA.MEDIA",
                            "necessity": "REQUIRED",
                            "purpose": (
                                "Enable video communication"
                            ),
                            "confidence": 0.82,
                        }
                    ],
                }
            ]
        }

    monkeypatch.setattr(
        "app.services.functional_baseline_service."
        "generate_functional_baseline_with_ai",
        fake_generator,
    )

    result = ensure_functional_baseline(
        session,
        application,
    )

    mappings = session.scalars(
        select(ExpectedMapping)
    ).all()

    assert result.source == BASELINE_AI_DERIVED
    assert result.available is True
    assert result.generated is True
    assert len(mappings) == 1
    assert mappings[0].source_version.startswith(
        BASELINE_AI_DERIVED
    )
    assert "policy" not in seen
    assert set(seen) == {
        "application_name",
        "category",
        "description",
    }


def test_ai_baseline_failure_falls_back_safely(monkeypatch):
    session = make_session()
    application = add_application(session)

    monkeypatch.setattr(
        "app.services.functional_baseline_service."
        "generate_functional_baseline_with_ai",
        lambda **kwargs: {"functions": []},
    )

    result = ensure_functional_baseline(
        session,
        application,
    )

    mappings = session.scalars(
        select(ExpectedMapping)
    ).all()

    assert result.source is None
    assert result.available is False
    assert result.status == "UNAVAILABLE"
    assert mappings == []


def test_ai_baseline_exception_is_non_fatal(monkeypatch):
    session = make_session()
    application = add_application(session)

    def fail(**kwargs):
        raise RuntimeError("model unavailable")

    monkeypatch.setattr(
        "app.services.functional_baseline_service."
        "generate_functional_baseline_with_ai",
        fail,
    )

    result = ensure_functional_baseline(
        session,
        application,
    )

    assert result.source is None
    assert result.available is False
    assert result.status == "FAILED"


def test_repeated_ai_baseline_does_not_duplicate(monkeypatch):
    session = make_session()
    application = add_application(session)

    monkeypatch.setattr(
        "app.services.functional_baseline_service."
        "generate_functional_baseline_with_ai",
        lambda **kwargs: {
            "functions": [
                {
                    "function_name": "Video Call",
                    "expected_data": [
                        {
                            "data_type": "DATA.MEDIA",
                            "necessity": "REQUIRED",
                            "purpose": (
                                "Enable video communication"
                            ),
                            "confidence": 0.8,
                        }
                    ],
                }
            ]
        },
    )

    ensure_functional_baseline(session, application)
    ensure_functional_baseline(session, application)

    mappings = session.scalars(
        select(ExpectedMapping)
    ).all()

    assert len(mappings) == 1


def test_ai_baseline_justification_is_persisted(monkeypatch):
    session = make_session()
    application = add_application(session)

    monkeypatch.setattr(
        "app.services.functional_baseline_service."
        "generate_functional_baseline_with_ai",
        lambda **kwargs: {
            "functions": [
                {
                    "function_name": "Video Call",
                    "expected_data": [
                        {
                            "data_type": "DATA.MEDIA",
                            "necessity": "REQUIRED",
                            "purpose": (
                                "Enable video communication"
                            ),
                            "justification": (
                                "Camera or media access is needed "
                                "for video communication."
                            ),
                            "confidence": 0.8,
                        }
                    ],
                }
            ]
        },
    )

    ensure_functional_baseline(session, application)

    mapping = session.scalars(
        select(ExpectedMapping)
    ).one()

    assert (
        mapping.baseline_justification
        == "Camera or media access is needed for video communication."
    )
