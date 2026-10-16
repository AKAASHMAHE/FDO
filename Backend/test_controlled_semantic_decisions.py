from app.ontology.semantic_decision_adapter import (
    decide_semantic_finding,
)


def test_semantic_not_fdo_when_declared_data_matches_expected_purpose():
    finding = {
        "application": "http://example.org/fdo#resource/application/NAV-01",
        "function": "Navigation",
        "expected_data": "precise_location",
        "declared_data": "precise_location",
        "expected_type": "precise_location",
        "declared_type": "precise_location",
        "expected_purpose": "navigation",
        "declared_purpose": "navigation",
    }

    decision = decide_semantic_finding(finding)

    assert decision.fdo_status == "NOT_FDO"
    assert decision.decision_reason
    assert decision.decision_confidence is not None
    assert 0.0 <= decision.decision_confidence <= 1.0


def test_semantic_ambiguous_when_declared_purpose_is_unclassified():
    finding = {
        "application": "http://example.org/fdo#resource/application/NAV-01",
        "function": "Navigation",
        "expected_data": "precise_location",
        "declared_data": "some_unclear_location_data",
        "expected_type": "precise_location",
        "declared_type": "unknown",
        "expected_purpose": "navigation",
        "declared_purpose": "unclear",
    }

    decision = decide_semantic_finding(finding)

    assert decision.fdo_status == "AMBIGUOUS"
    assert decision.decision_reason
    assert decision.decision_confidence is not None
    assert 0.0 <= decision.decision_confidence <= 1.0


def test_semantic_ambiguous_when_declared_context_is_unclear():
    finding = {
        "application": "http://example.org/fdo#resource/application/NAV-01",
        "function": "Navigation",
        "expected_data": "precise_location",
        "declared_data": "some_unclear_location_data",
        "expected_type": "precise_location",
        "declared_type": "unknown",
        "expected_purpose": "navigation",
        "declared_purpose": "unclear",
    }

    decision = decide_semantic_finding(finding)

    assert decision.fdo_status == "AMBIGUOUS"
    assert decision.decision_reason