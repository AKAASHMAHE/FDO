from app.ontology.db_semantic_analysis_service import (
    DBSemanticAnalysisService,
)


def test_db_semantic_analysis_service_detects_fdo(
    tmp_path,
):

    service = DBSemanticAnalysisService()

    results = service.analyze(
        application={
            "application_id": "semantic-app-001",
            "application_name": "Semantic Navigation App",
            "category": "Navigation",
            "description": "Semantic integration test",
        },
        functions=[
            {
                "function_record_id": "semantic-func-001",
                "function_id": "navigation",
                "application_id": "semantic-app-001",
                "function_name": "Navigation",
                "description": "Navigation feature",
            }
        ],
        expected_data=[
            {
                "expected_id": "semantic-expected-001",
                "application_id": "semantic-app-001",
                "function_record_id": "semantic-func-001",
                "data_type": "location",
                "necessity": "required",
                "expected_purpose": "navigation",
            }
        ],
        declared_data=[
            {
                "evidence_id": "semantic-declared-001",
                "policy_id": "semantic-policy-001",
                "data_type": "precise_location",
                "purpose": "advertising",
                "sharing": "third parties",
                "retention": "30 days",
            }
        ],
        output_path=(
            tmp_path / "semantic-analysis.ttl"
        ),
    )

    matching = [
        result
        for result in results
        if result["application"].endswith(
            "/application/semantic-app-001"
        )
    ]

    assert len(matching) >= 1

    result = matching[0]

    assert result["expected_type"] == "location"
    assert (
        result["declared_type"]
        == "precise_location"
    )

    assert result["expected_purpose"] == "navigation"
    assert (
        result["declared_purpose"]
        == "advertising"
    )

    assert result["fdo_status"] == "FDO"
    assert result["confidence"] == 0.80
    assert result["reason"]