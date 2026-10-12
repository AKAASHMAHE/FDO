from fastapi.testclient import TestClient

from app.main import app
from test_helpers import fake_google_maps_baseline


def test_plural_analysis_get_returns_persisted_semantic_results(
    monkeypatch,
):
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

    post_response = client.post(
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

    assert post_response.status_code == 200, post_response.text

    post_body = post_response.json()
    analysis_id = post_body["analysis_id"]

    assert len(post_body["semantic_results"]) > 0

    get_response = client.get(
        f"/api/v1/analyses/{analysis_id}"
    )

    assert get_response.status_code == 200, get_response.text

    get_body = get_response.json()

    assert "semantic_results" in get_body
    assert isinstance(get_body["semantic_results"], list)

    assert len(get_body["semantic_results"]) == len(
        post_body["semantic_results"]
    )

    for result in get_body["semantic_results"]:
        assert result["application_id"] == "NAV-01"
        assert result["fdo_status"] in {
            "FDO",
            "NOT_FDO",
            "AMBIGUOUS",
        }
        assert result["confidence"] is not None
        assert 0.0 <= result["confidence"] <= 1.0