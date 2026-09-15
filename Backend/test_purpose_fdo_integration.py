from types import SimpleNamespace

from app.services.comparison_service import build_comparison
from app.services.fdo_decision_service import (
    FDODecisionInput,
    evaluate_fdo_decision,
)


def create_expected():
    return SimpleNamespace(
        expected_id="TEST-EXP-001",
        application_id="TEST-APP-001",
        function_record_id="TEST-FUNC-001",
        data_type="DATA.LOCATION.PRECISE",
        necessity="REQUIRED",
        expected_purpose="navigation",
    )


def create_evidence(
    purpose="directions and nearby search",
):
    return SimpleNamespace(
        evidence_id="TEST-EVIDENCE-001",
        data_type="DATA.LOCATION.PRECISE",
        purpose=purpose,
        sharing="NO",
        retention="NOT_SPECIFIED",
        extraction_status="EXTRACTED",
    )


def test_semantic_purpose_reaches_fdo_decision():
    expected = create_expected()
    evidence = create_evidence()

    comparison = build_comparison(
        expected,
        evidence,
    )

    assert comparison.data_match == "EXACT_MATCH"
    assert comparison.purpose_compatibility == "COMPATIBLE"
    assert comparison.functional_relationship == "RELATED"
    assert comparison.evidence_status == "EXTRACTED"

    decision_input = FDODecisionInput(
        expected_id=expected.expected_id,
        application_id=expected.application_id,
        expected_data_type=expected.data_type,
        expected_necessity=expected.necessity,
        expected_purpose=expected.expected_purpose,
        declared_evidence_id=evidence.evidence_id,
        declared_data_type=evidence.data_type,
        declared_purpose=evidence.purpose,
        data_match=comparison.data_match,
        purpose_compatibility=comparison.purpose_compatibility,
        functional_relationship=comparison.functional_relationship,
        evidence_status=comparison.evidence_status,
    )

    decision = evaluate_fdo_decision(
        decision_input
    )

    assert decision.fdo_status == "NOT_FDO"


def test_incompatible_purpose_reaches_fdo_decision():
    expected = create_expected()

    evidence = create_evidence(
        purpose="targeted advertising"
    )

    comparison = build_comparison(
        expected,
        evidence,
    )

    assert comparison.data_match == "EXACT_MATCH"
    assert comparison.purpose_compatibility == "INCOMPATIBLE"
    assert comparison.functional_relationship == "RELATED"
    assert comparison.evidence_status == "EXTRACTED"

    decision_input = FDODecisionInput(
        expected_id=expected.expected_id,
        application_id=expected.application_id,
        expected_data_type=expected.data_type,
        expected_necessity=expected.necessity,
        expected_purpose=expected.expected_purpose,
        declared_evidence_id=evidence.evidence_id,
        declared_data_type=evidence.data_type,
        declared_purpose=evidence.purpose,
        data_match=comparison.data_match,
        purpose_compatibility=comparison.purpose_compatibility,
        functional_relationship=comparison.functional_relationship,
        evidence_status=comparison.evidence_status,
    )

    decision = evaluate_fdo_decision(
        decision_input
    )

    assert decision.fdo_status == "FDO"