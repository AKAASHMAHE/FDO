from types import SimpleNamespace

from app.ontology.semantic_explanation_service import (
    build_semantic_explanation,
)


def test_semantic_fdo_explanation():
    result = SimpleNamespace(
        fdo_status="FDO",
        function="Navigation",
        expected_data="precise_location",
        declared_data="device_location",
        expected_purpose="navigation",
        declared_purpose="advertising",
        reason="The declared data purpose is incompatible with the expected functional purpose.",
        confidence=0.85,
    )

    explanation = build_semantic_explanation(result)

    assert "Functional Data Overreach (FDO) was detected." in explanation
    assert "Navigation" in explanation
    assert "precise_location" in explanation
    assert "device_location" in explanation
    assert "navigation" in explanation
    assert "advertising" in explanation
    assert result.reason in explanation
    assert "0.85" in explanation


def test_semantic_not_fdo_explanation():
    result = SimpleNamespace(
        fdo_status="NOT_FDO",
        function="Navigation",
        expected_data="precise_location",
        declared_data="precise_location",
        expected_purpose="navigation",
        declared_purpose="navigation",
        reason="The declared data and purpose match the expected functional requirements.",
        confidence=0.90,
    )

    explanation = build_semantic_explanation(result)

    assert "No Functional Data Overreach (FDO) was detected." in explanation
    assert "Navigation" in explanation
    assert "precise_location" in explanation
    assert "navigation" in explanation
    assert result.reason in explanation
    assert "0.90" in explanation


def test_semantic_ambiguous_explanation():
    result = SimpleNamespace(
        fdo_status="AMBIGUOUS",
        function="Navigation",
        expected_data="precise_location",
        declared_data="unknown",
        expected_purpose="navigation",
        declared_purpose="unclear",
        reason="The available comparison evidence does not satisfy a deterministic FDO or NOT_FDO rule.",
        confidence=0.50,
    )

    explanation = build_semantic_explanation(result)

    assert "ambiguous result" in explanation
    assert "Navigation" in explanation
    assert "precise_location" in explanation
    assert "unknown" in explanation
    assert "unclear" in explanation
    assert result.reason in explanation
    assert "0.50" in explanation