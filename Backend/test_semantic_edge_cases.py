from types import SimpleNamespace

from app.ontology.semantic_decision_adapter import (
    decide_semantic_finding,
)
from app.ontology.semantic_explanation_service import (
    build_semantic_explanation,
)


def test_missing_declared_type_is_handled():
    finding = {
        "application": "http://example.org/fdo#resource/application/NAV-01",
        "function": "Navigation",
        "expected_data": "precise_location",
        "declared_data": "device_location",
        "expected_type": "precise_location",
        "declared_type": None,
        "expected_purpose": "navigation",
        "declared_purpose": "navigation",
    }

    decision = decide_semantic_finding(finding)

    assert decision.fdo_status in {"FDO", "AMBIGUOUS"}
    assert decision.decision_reason
    assert decision.decision_confidence is not None


def test_missing_declared_purpose_is_handled():
    finding = {
        "application": "http://example.org/fdo#resource/application/NAV-01",
        "function": "Navigation",
        "expected_data": "precise_location",
        "declared_data": "precise_location",
        "expected_type": "precise_location",
        "declared_type": "precise_location",
        "expected_purpose": "navigation",
        "declared_purpose": None,
    }

    decision = decide_semantic_finding(finding)

    assert decision.fdo_status in {"FDO", "AMBIGUOUS"}
    assert decision.decision_reason
    assert decision.decision_confidence is not None


def test_missing_expected_type_is_handled():
    finding = {
        "application": "http://example.org/fdo#resource/application/NAV-01",
        "function": "Navigation",
        "expected_data": "precise_location",
        "declared_data": "device_location",
        "expected_type": None,
        "declared_type": "device_location",
        "expected_purpose": "navigation",
        "declared_purpose": "navigation",
    }

    decision = decide_semantic_finding(finding)

    assert decision.fdo_status in {"FDO", "AMBIGUOUS"}
    assert decision.decision_reason
    assert decision.decision_confidence is not None


def test_missing_expected_purpose_is_handled():
    finding = {
        "application": "http://example.org/fdo#resource/application/NAV-01",
        "function": "Navigation",
        "expected_data": "precise_location",
        "declared_data": "precise_location",
        "expected_type": "precise_location",
        "declared_type": "precise_location",
        "expected_purpose": None,
        "declared_purpose": "navigation",
    }

    decision = decide_semantic_finding(finding)

    assert decision.fdo_status in {"FDO", "AMBIGUOUS"}
    assert decision.decision_reason
    assert decision.decision_confidence is not None


def test_empty_semantic_finding_does_not_crash():
    decision = decide_semantic_finding({})

    assert decision.fdo_status in {"FDO", "AMBIGUOUS", "NOT_FDO"}
    assert decision.decision_reason
    assert decision.decision_confidence is not None


def test_semantic_explanation_without_confidence():
    result = SimpleNamespace(
        fdo_status="FDO",
        function="Navigation",
        expected_data="precise_location",
        declared_data="device_location",
        expected_purpose="navigation",
        declared_purpose="advertising",
        reason="Declared purpose is incompatible with the expected functional purpose.",
        confidence=None,
    )

    explanation = build_semantic_explanation(result)

    assert "Functional Data Overreach (FDO) was detected." in explanation
    assert "Navigation" in explanation
    assert "precise_location" in explanation
    assert "device_location" in explanation
    assert "advertising" in explanation
    assert result.reason in explanation


def test_semantic_explanation_unknown_status():
    result = SimpleNamespace(
        fdo_status="UNKNOWN",
        function="Navigation",
        expected_data="precise_location",
        declared_data="device_location",
        expected_purpose="navigation",
        declared_purpose="unknown",
        reason="Unknown semantic decision state.",
        confidence=None,
    )

    explanation = build_semantic_explanation(result)

    assert "ambiguous result" in explanation
    assert result.reason in explanation