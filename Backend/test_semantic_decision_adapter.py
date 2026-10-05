from app.ontology.semantic_decision_adapter import (
    decide_semantic_finding,
    semantic_finding_to_decision_input,
)


def test_semantic_finding_maps_to_no_match():
    finding = {
        "expected_data": "location",
        "declared_data": "location",
        "expected_type": "location",
        "declared_type": "precise_location",
        "expected_purpose": "navigation",
        "declared_purpose": "advertising",
    }

    decision_input = semantic_finding_to_decision_input(finding)

    assert decision_input.data_match == "NO_MATCH"
    assert decision_input.purpose_compatibility == "INCOMPATIBLE"
    assert decision_input.functional_relationship == "RELATED"
    assert decision_input.evidence_status == "EXTRACTED"


def test_semantic_finding_reaches_existing_fdo_engine():
    finding = {
        "expected_data": "location",
        "declared_data": "location",
        "expected_type": "location",
        "declared_type": "precise_location",
        "expected_purpose": "navigation",
        "declared_purpose": "advertising",
    }

    decision = decide_semantic_finding(finding)

    assert decision.fdo_status == "FDO"
    assert decision.decision_confidence == 0.80


def test_matching_semantic_data_reaches_not_fdo():
    finding = {
        "expected_data": "phone-number",
        "declared_data": "phone-number",
        "expected_type": "phone_number",
        "declared_type": "phone_number",
        "expected_purpose": "communication",
        "declared_purpose": "communication",
    }

    decision = decide_semantic_finding(finding)

    assert decision.fdo_status == "NOT_FDO"
    assert decision.decision_confidence == 0.90