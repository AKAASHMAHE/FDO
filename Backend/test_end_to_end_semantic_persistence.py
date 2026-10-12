from fastapi.testclient import TestClient

from app.main import app
from test_helpers import fake_google_maps_baseline


def test_end_to_end_semantic_persistence(monkeypatch):
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

    analyze_response = client.post(
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

    assert analyze_response.status_code == 200

    analyze_body = analyze_response.json()

    analysis_id = analyze_body["analysis_id"]

    semantic_results_from_analyze = (
        analyze_body["semantic_results"]
    )

    assert len(semantic_results_from_analyze) > 0

    # Retrieve the persisted analysis independently.
    report_response = client.get(
        f"/api/v1/analysis/{analysis_id}"
    )

    assert report_response.status_code == 200

    report_body = report_response.json()

    assert report_body["analysis_id"] == analysis_id

    assert "semantic_results" in report_body

    persisted_results = report_body["semantic_results"]

    assert len(persisted_results) == len(
        semantic_results_from_analyze
    )

    for original, persisted in zip(
        semantic_results_from_analyze,
        persisted_results,
    ):
        assert persisted["application_id"] == original[
            "application_id"
        ]

        assert persisted["application"] == original[
            "application"
        ]

        assert persisted["function"] == original[
            "function"
        ]

        assert persisted["expected_data"] == original[
            "expected_data"
        ]

        assert persisted["declared_data"] == original[
            "declared_data"
        ]

        assert persisted["expected_type"] == original[
            "expected_type"
        ]

        assert persisted["declared_type"] == original[
            "declared_type"
        ]

        assert persisted["expected_purpose"] == original[
            "expected_purpose"
        ]

        assert persisted["declared_purpose"] == original[
            "declared_purpose"
        ]

        assert persisted["fdo_status"] == original[
            "fdo_status"
        ]

        assert persisted["confidence"] == original[
            "confidence"
        ]

        assert persisted["reason"] == original[
            "reason"
        ]