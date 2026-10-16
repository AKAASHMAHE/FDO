from app.ontology.semantic_result_service import (
    SemanticResultService,
)

from test_fuseki_fixture import (
    setup_fuseki_semantic_fixture,
)


def setup_module():
    setup_fuseki_semantic_fixture()


def test_semantic_result_contains_explanation():
    service = SemanticResultService()

    results = service.analyze()

    assert len(results) >= 1

    result = results[0]

    assert result["application"].endswith(
        "/application/app-001"
    )

    assert result["function"].endswith(
        "/function/func-001"
    )

    assert result["expected_type"] == "location"
    assert result["declared_type"] == "precise_location"

    assert result["expected_purpose"] == "navigation"
    assert result["declared_purpose"] == "advertising"

    assert result["fdo_status"] == "FDO"
    assert result["confidence"] == 0.85
    assert result["data_match_relation"] == "NARROWER_EVIDENCE"

    assert result["reason"]