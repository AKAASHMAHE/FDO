"""
Adapter between semantic RDF findings and the existing FDO decision engine.
"""

from app.services.fdo_decision_service import (
    FDODecisionInput,
    FDODecisionOutput,
    evaluate_fdo_decision,
)


def semantic_finding_to_decision_input(
    finding: dict,
) -> FDODecisionInput:
    """
    Convert a semantic SPARQL finding into the existing
    deterministic FDO decision input.

    Semantic findings do not contain application/function/evidence
    context, so those fields are represented conservatively.
    """

    expected_type = finding.get("expected_type")
    declared_type = finding.get("declared_type")
    expected_purpose = finding.get("expected_purpose")
    declared_purpose = finding.get("declared_purpose")

    data_match = (
        "EXACT_MATCH"
        if expected_type == declared_type
        else "NO_MATCH"
    )

    purpose_compatibility = (
        "COMPATIBLE"
        if expected_purpose == declared_purpose
        else "INCOMPATIBLE"
    )

    return FDODecisionInput(
        expected_id=str(finding.get("expected_data", "")),
        application_id=str(finding.get("application_id", "semantic")),
        expected_data_type=str(expected_type or ""),
        expected_necessity=str(
            finding.get("expected_necessity", "unknown")
        ),
        expected_purpose=str(expected_purpose or ""),
        declared_evidence_id=finding.get("declared_evidence_id"),
        declared_data_type=(
            str(declared_type)
            if declared_type is not None
            else None
        ),
        declared_purpose=(
            str(declared_purpose)
            if declared_purpose is not None
            else None
        ),
        data_match=data_match,
        purpose_compatibility=purpose_compatibility,
        functional_relationship="RELATED",
        evidence_status="EXTRACTED",
    )


def decide_semantic_finding(
    finding: dict,
) -> FDODecisionOutput:
    """
    Pass a semantic finding through the existing
    deterministic FDO decision engine.
    """

    decision_input = semantic_finding_to_decision_input(finding)

    return evaluate_fdo_decision(decision_input)