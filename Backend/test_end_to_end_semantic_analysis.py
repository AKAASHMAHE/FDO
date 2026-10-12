from fastapi.testclient import TestClient

from app.main import app
from test_helpers import fake_google_maps_baseline


def test_end_to_end_semantic_analysis(monkeypatch):
    fake_evidence = [
        {
            "data_type": "DATA.LOCATION.PRECISE",
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
        "app.services.functional_baseline_service.generate_functional_baseline_with_ai",
        fake_google_maps_baseline,
    )
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

    # Core analysis response
    assert body["analysis_id"]
    assert body["application_id"] == "NAV-01"
    assert body["analysis_status"]

    # Relational analysis
    assert "comparisons" in body
    assert "fdo_results" in body

    # Semantic analysis
    assert "semantic_results" in body
    assert isinstance(body["semantic_results"], list)

    assert len(body["semantic_results"]) > 0

    for result in body["semantic_results"]:
        assert result["application_id"] == "NAV-01"

        assert result["application"]
        assert result["function"]

        assert result["expected_data"]
        assert result["declared_data"]

        assert result["expected_type"]
        assert result["declared_type"]

        assert result["expected_purpose"]
        assert result["declared_purpose"]

        assert result["fdo_status"] in {
            "FDO",
            "NOT_FDO",
            "AMBIGUOUS",
        }

        assert result["reason"]

        if result["confidence"] is not None:
            assert 0.0 <= result["confidence"] <= 1.0