from types import SimpleNamespace

from app.ontology.semantic_explanation_service import (
    build_semantic_explanation,
)


def test_build_semantic_explanation_for_fdo():
    result = SimpleNamespace(
        function="Turn-by-turn navigation",
        expected_data="DATA.LOCATION.PRECISE",
        declared_data="DATA.LOCATION.PRECISE",
        expected_purpose="Route/navigation",
        declared_purpose="Advertising",
        fdo_status="FDO",
        confidence=0.95,
        reason=(
            "Declared purpose is not aligned with "
            "the expected functional purpose."
        ),
    )

    explanation = build_semantic_explanation(result)

    assert "Functional Data Overreach (FDO) was detected." in explanation
    assert "Turn-by-turn navigation" in explanation
    assert "DATA.LOCATION.PRECISE" in explanation
    assert "Route/navigation" in explanation
    assert "Advertising" in explanation
    assert "Declared purpose is not aligned" in explanation
    assert "0.95" in explanation


def test_build_semantic_explanation_for_not_fdo():
    result = SimpleNamespace(
        function="Turn-by-turn navigation",
        expected_data="DATA.LOCATION.PRECISE",
        declared_data="DATA.LOCATION.PRECISE",
        expected_purpose="Route/navigation",
        declared_purpose="Route/navigation",
        fdo_status="NOT_FDO",
        confidence=0.98,
        reason="Declared processing aligns with expected use.",
    )

    explanation = build_semantic_explanation(result)

    assert "No Functional Data Overreach (FDO) was detected." in explanation
    assert "Declared processing aligns with expected use." in explanation
    assert "0.98" in explanation


def test_build_semantic_explanation_for_ambiguous():
    result = SimpleNamespace(
        function="Location search",
        expected_data="DATA.LOCATION.APPROXIMATE",
        declared_data="DATA.LOCATION.PRECISE",
        expected_purpose="Search/localization",
        declared_purpose="Unknown",
        fdo_status="AMBIGUOUS",
        confidence=None,
        reason="Evidence was insufficient.",
    )

    explanation = build_semantic_explanation(result)

    assert "ambiguous result" in explanation
    assert "Evidence was insufficient." in explanation
    assert "Decision confidence" not in explanation