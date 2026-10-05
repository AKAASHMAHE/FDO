from fastapi.testclient import TestClient
from sqlalchemy import inspect

from app.main import app
from app.database import engine


def test_semantic_results_are_persisted_in_database(
    monkeypatch,
):
    fake_evidence = [
        {
            "data_type": "precise_location",
            "purpose": "advertising",
            "entity": "third_party_advertiser",
            "sharing": "shared",
            "retention": "30 days",
            "evidence_text": (
                "The application may collect precise location "
                "information for advertising purposes."
            ),
            "source_section": "Data Collection",
            "extraction_status": "EXTRACTED",
            "confidence": 0.95,
        }
    ]

    monkeypatch.setattr(
        "app.main.extract_policy_evidence",
        lambda policy_text, application_name: fake_evidence,
    )

    client = TestClient(app)

    response = client.post(
        "/api/v1/analyze",
        json={
            "application_name": "Google Maps",
            "category": "Navigation",
            "description": "Navigation application",
            "policy_text": (
                "The application may collect precise location "
                "information for advertising purposes."
            ),
            "policy_source": "TEST",
        },
    )

    assert response.status_code == 200, response.text

    body = response.json()

    analysis_id = body["analysis_id"]

    semantic_results = body["semantic_results"]

    assert len(semantic_results) > 0

    # Verify the semantic table exists.
    inspector = inspect(engine)

    tables = inspector.get_table_names()

    assert "semantic_fdo_results" in tables

    # Open the real application database.
    from app.database import SessionLocal
    from app.models.semantic_fdo_result import SemanticFDOResult

    db = SessionLocal()

    try:
        persisted = (
            db.query(SemanticFDOResult)
            .filter(
                SemanticFDOResult.analysis_id
                == analysis_id
            )
            .order_by(
                SemanticFDOResult.semantic_result_id
            )
            .all()
        )

        assert len(persisted) == len(
            semantic_results
        )

        for db_result, api_result in zip(
            persisted,
            semantic_results,
        ):
            assert (
                db_result.semantic_result_id
                == api_result["semantic_result_id"]
            )

            assert (
                db_result.analysis_id
                == analysis_id
            )

            assert (
                db_result.application_id
                == api_result["application_id"]
            )

            assert (
                db_result.fdo_status
                == api_result["fdo_status"]
            )

            assert (
                db_result.reason
                == api_result["reason"]
            )

    finally:
        db.close()