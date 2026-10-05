from fastapi.testclient import TestClient

from app.main import app


def test_semantic_results_persist_and_are_returned_by_get(monkeypatch):
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

    # 1. Run analysis
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

    assert "semantic_results" in post_body
    assert len(post_body["semantic_results"]) > 0

    posted_results = post_body["semantic_results"]

    # 2. Fetch the same analysis using GET
    get_response = client.get(
        f"/api/v1/analysis/{analysis_id}"
    )

    assert get_response.status_code == 200, get_response.text

    get_body = get_response.json()

    # 3. Confirm semantic results are returned
    assert "semantic_results" in get_body
    assert isinstance(get_body["semantic_results"], list)

    # 4. Confirm GET results match persisted POST results
    assert len(get_body["semantic_results"]) == len(posted_results)

    for post_result, get_result in zip(
        posted_results,
        get_body["semantic_results"],
    ):
        assert get_result["application_id"] == post_result["application_id"]
        assert get_result["application"] == post_result["application"]
        assert get_result["function"] == post_result["function"]
        assert get_result["expected_data"] == post_result["expected_data"]
        assert get_result["declared_data"] == post_result["declared_data"]
        assert get_result["expected_type"] == post_result["expected_type"]
        assert get_result["declared_type"] == post_result["declared_type"]
        assert get_result["expected_purpose"] == post_result["expected_purpose"]
        assert get_result["declared_purpose"] == post_result["declared_purpose"]
        assert get_result["fdo_status"] == post_result["fdo_status"]
        assert get_result["confidence"] == post_result["confidence"]
        assert get_result["reason"] == post_result["reason"]

    print("\nPersisted semantic results successfully returned by GET:")
    for result in get_body["semantic_results"]:
        print(result)