from fastapi.testclient import TestClient

from app.main import app


def test_rich_report_contains_semantic_explanations(
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

    analysis_id = post_response.json()["analysis_id"]

    response = client.get(
        f"/api/v1/analysis/{analysis_id}/report"
    )

    assert response.status_code == 200, response.text

    body = response.json()

    assert "semantic_results" in body
    assert isinstance(body["semantic_results"], list)

    assert len(body["semantic_results"]) > 0

    for result in body["semantic_results"]:
        assert "semantic_result_id" in result
        assert "application_id" in result
        assert "application" in result
        assert "function" in result
        assert "expected_data" in result
        assert "declared_data" in result
        assert "expected_purpose" in result
        assert "declared_purpose" in result
        assert "fdo_status" in result
        assert "confidence" in result
        assert "reason" in result
        assert "explanation" in result

        assert result["explanation"]

        if result["fdo_status"] == "FDO":
            assert (
                "Functional Data Overreach (FDO) was detected."
                in result["explanation"]
            )

    print("\nSemantic rich-report results:")
    for result in body["semantic_results"]:
        print(result)