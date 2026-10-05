from app.ontology.fuseki_semantic_detector import (
    FusekiSemanticDetector,
)

from test_fuseki_fixture import (
    setup_fuseki_semantic_fixture,
)


def setup_module():
    setup_fuseki_semantic_fixture()


def test_fuseki_semantic_detector_finds_fdo():
    detector = FusekiSemanticDetector()

    findings = detector.detect_fdo()

    assert len(findings) >= 1

    finding = findings[0]

    assert finding["expected_type"] == "location"
    assert finding["declared_type"] == "precise_location"

    assert finding["expected_purpose"] == "navigation"
    assert finding["declared_purpose"] == "advertising"