from fastapi.testclient import TestClient

from app.main import app


def test_semantic_and_relational_results_share_analysis_context(
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
    application_id = body["application_id"]

    comparisons = body["comparisons"]
    fdo_results = body["fdo_results"]
    semantic_results = body["semantic_results"]

    # Both analysis layers must produce output.
    assert len(comparisons) > 0
    assert len(fdo_results) > 0
    assert len(semantic_results) > 0

    # The API response belongs to one analysis/application context.
    assert analysis_id
    assert application_id == "NAV-01"

    # Every semantic result must belong to the same application.
    for result in semantic_results:
        assert result["application_id"] == application_id

    # Every relational FDO result must have a valid decision.
    for result in fdo_results:
        assert result["fdo_status"] in {
            "FDO",
            "NOT_FDO",
            "AMBIGUOUS",
        }

        if result["decision_confidence"] is not None:
            assert 0.0 <= result["decision_confidence"] <= 1.0

    # Every semantic result must also have a valid decision.
    for result in semantic_results:
        assert result["fdo_status"] in {
            "FDO",
            "NOT_FDO",
            "AMBIGUOUS",
        }

        if result["confidence"] is not None:
            assert 0.0 <= result["confidence"] <= 1.0

    # Semantic results must contain an explainable reason.
    for result in semantic_results:
        assert result["reason"]