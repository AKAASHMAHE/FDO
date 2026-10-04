from types import SimpleNamespace

from app.services.comparison_service import build_comparison
from app.services.fdo_decision_service import (
    FDODecisionInput,
    evaluate_fdo_decision,
)


def create_expected():
    return SimpleNamespace(
        expected_id="EXP-001",
        application_id="APP-001",
        data_type="DATA.LOCATION.PRECISE",
        necessity="REQUIRED",
        expected_purpose="navigation",
        function_record_id="NAV-01",
    )


def create_evidence(
    purpose="directions",
):
    return SimpleNamespace(
        evidence_id="EVID-001",
        data_type="DATA.LOCATION.PRECISE",
        purpose=purpose,
        function="NAV-01",
        sharing="third_party",
        retention="30 days",
        extraction_status="EXTRACTED",
    )


def build_decision_input(expected, evidence, comparison):
    return FDODecisionInput(
        expected_id=comparison.expected_id,
        application_id=expected.application_id,
        expected_data_type=expected.data_type,
        expected_necessity=expected.necessity,
        expected_purpose=expected.expected_purpose,
        declared_evidence_id=comparison.declared_evidence_id,
        declared_data_type=evidence.data_type,
        declared_purpose=evidence.purpose,
        data_match=comparison.data_match,
        purpose_compatibility=comparison.purpose_compatibility,
        functional_relationship=comparison.functional_relationship,
        evidence_status=comparison.evidence_status,
    )


def test_semantic_purpose_reaches_fdo_decision():
    expected = create_expected()

    evidence = create_evidence(
        purpose="directions and route guidance",
    )

    comparison = build_comparison(
        expected,
        evidence,
    )

    assert comparison.data_match == "EXACT_MATCH"
    assert comparison.purpose_compatibility == "COMPATIBLE"
    assert comparison.functional_relationship == "RELATED"
    assert comparison.evidence_status == "EXTRACTED"

    decision_input = build_decision_input(
        expected,
        evidence,
        comparison,
    )

    decision = evaluate_fdo_decision(
        decision_input,
    )

    assert decision.fdo_status == "NOT_FDO"


def test_incompatible_purpose_reaches_fdo_decision():
    expected = create_expected()

    evidence = create_evidence(
        purpose="targeted advertising",
    )

    comparison = build_comparison(
        expected,
        evidence,
    )

    assert comparison.data_match == "EXACT_MATCH"
    assert comparison.purpose_compatibility == "INCOMPATIBLE"
    assert comparison.functional_relationship == "RELATED"
    assert comparison.evidence_status == "EXTRACTED"

    decision_input = build_decision_input(
        expected,
        evidence,
        comparison,
    )

    decision = evaluate_fdo_decision(
        decision_input,
    )

    assert decision.fdo_status == "FDO"


def test_multi_purpose_compatible_results_in_not_fdo():
    expected = SimpleNamespace(
        expected_id="EXP-001",
        application_id="APP-001",
        data_type="DATA.LOCATION.PRECISE",
        necessity="REQUIRED",
        expected_purpose="navigation",
        function_record_id="NAV-01",
    )

    evidence = SimpleNamespace(
        evidence_id="EVID-001",
        data_type="DATA.LOCATION.PRECISE",
        purpose="directions and targeted advertising",
        function="NAV-01",
        sharing="third_party",
        retention="30 days",
        extraction_status="EXTRACTED",
    )

    comparison = build_comparison(
        expected,
        evidence,
    )

    assert comparison.data_match == "EXACT_MATCH"
    assert comparison.purpose_compatibility == "COMPATIBLE"
    assert comparison.functional_relationship == "RELATED"
    assert comparison.evidence_status == "EXTRACTED"

    decision_input = build_decision_input(
        expected,
        evidence,
        comparison,
    )

    decision = evaluate_fdo_decision(
        decision_input,
    )

    assert decision.fdo_status == "NOT_FDO"


def test_multi_purpose_incompatible_results_in_fdo():
    expected = SimpleNamespace(
        expected_id="EXP-002",
        application_id="APP-001",
        data_type="DATA.LOCATION.PRECISE",
        necessity="REQUIRED",
        expected_purpose="navigation",
        function_record_id="NAV-01",
    )

    evidence = SimpleNamespace(
        evidence_id="EVID-002",
        data_type="DATA.LOCATION.PRECISE",
        purpose="targeted advertising and marketing",
        function="NAV-01",
        sharing="third_party",
        retention="30 days",
        extraction_status="EXTRACTED",
    )

    comparison = build_comparison(
        expected,
        evidence,
    )

    assert comparison.data_match == "EXACT_MATCH"
    assert comparison.purpose_compatibility == "INCOMPATIBLE"
    assert comparison.functional_relationship == "RELATED"
    assert comparison.evidence_status == "EXTRACTED"

    decision_input = build_decision_input(
        expected,
        evidence,
        comparison,
    )

    decision = evaluate_fdo_decision(
        decision_input,
    )

    assert decision.fdo_status == "FDO"