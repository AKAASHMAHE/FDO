from fastapi.testclient import TestClient

from app.main import app


def test_analyze_endpoint_returns_semantic_results(
    monkeypatch,
    isolated_app_database,
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

    assert "semantic_results" in body
    assert isinstance(body["semantic_results"], list)

    for result in body["semantic_results"]:
        assert "application_id" in result
        assert "application" in result
        assert "function" in result
        assert "expected_data" in result
        assert "declared_data" in result
        assert "expected_type" in result
        assert "declared_type" in result
        assert "expected_purpose" in result
        assert "declared_purpose" in result
        assert "fdo_status" in result
        assert "confidence" in result
        assert "reason" in result

        assert result["application_id"] == "NAV-01"

        assert result["fdo_status"] in {
            "FDO",
            "NOT_FDO",
            "AMBIGUOUS",
        }

        if result["confidence"] is not None:
            assert 0.0 <= result["confidence"] <= 1.0

    print("\nAPI semantic results:")
    for result in body["semantic_results"]:
        print(result)