from app.ontology.semantic_analysis_service import (
    SemanticAnalysisService,
)

from test_fuseki_fixture import (
    setup_fuseki_semantic_fixture,
)


def setup_module():
    setup_fuseki_semantic_fixture()


def test_semantic_analysis_service_returns_fdo_result():
    service = SemanticAnalysisService()

    results = service.analyze()

    assert len(results) >= 1

    result = results[0]

    assert result["fdo_status"] == "FDO"
    assert result["confidence"] == 0.80
    assert result["expected_type"] == "location"
    assert result["declared_type"] == "precise_location"
    assert result["expected_purpose"] == "navigation"
    assert result["declared_purpose"] == "advertising"
    assert result["reason"]