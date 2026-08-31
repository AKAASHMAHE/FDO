from dataclasses import dataclass


@dataclass
class FDODecisionInput:
    expected_id: str
    application_id: str
    expected_data_type: str
    expected_necessity: str
    expected_purpose: str

    declared_evidence_id: str | None
    declared_data_type: str | None
    declared_purpose: str | None

    data_match: str
    purpose_compatibility: str
    functional_relationship: str
    evidence_status: str


@dataclass
class FDODecisionOutput:
    fdo_status: str
    decision_reason: str
    decision_confidence: float | None
def evaluate_fdo_decision(
    comparison: FDODecisionInput,
) -> FDODecisionOutput:
    """
    Deterministic baseline FDO decision logic.

    Returns:
        FDO
        NOT_FDO
        AMBIGUOUS
    """

    # ---------------------------------------------------------
    # Rule 1: No declared evidence
    # ---------------------------------------------------------
    if comparison.evidence_status == "NO_EVIDENCE":
        return FDODecisionOutput(
            fdo_status="AMBIGUOUS",
            decision_reason=(
                "No declared evidence is available to determine "
                "whether the data collection is functionally "
                "justified."
            ),
            decision_confidence=0.30,
        )

    # ---------------------------------------------------------
    # Rule 2: Evidence exists but is insufficient/unknown
    # ---------------------------------------------------------
    if comparison.evidence_status in {
        "INSUFFICIENT",
        "UNKNOWN",
    }:
        return FDODecisionOutput(
            fdo_status="AMBIGUOUS",
            decision_reason=(
                "Evidence is insufficient to make a "
                "deterministic FDO decision."
            ),
            decision_confidence=0.40,
        )

    # ---------------------------------------------------------
    # Rules below require extracted evidence.
    # ---------------------------------------------------------
    if comparison.evidence_status != "EXTRACTED":
        return FDODecisionOutput(
            fdo_status="AMBIGUOUS",
            decision_reason=(
                "Evidence status does not support a "
                "deterministic FDO decision."
            ),
            decision_confidence=0.40,
        )

    # ---------------------------------------------------------
    # Rule 3: Exact data + compatible purpose + related
    # ---------------------------------------------------------
    if (
        comparison.data_match == "EXACT_MATCH"
        and comparison.purpose_compatibility == "COMPATIBLE"
        and comparison.functional_relationship == "RELATED"
    ):
        return FDODecisionOutput(
            fdo_status="NOT_FDO",
            decision_reason=(
                "The declared data type matches the expected "
                "data type, the declared purpose is compatible "
                "with the expected purpose, and evidence is "
                "available for the function."
            ),
            decision_confidence=0.90,
        )

    # ---------------------------------------------------------
    # Rule 4: Exact data + incompatible purpose + related
    # ---------------------------------------------------------
    if (
        comparison.data_match == "EXACT_MATCH"
        and comparison.purpose_compatibility == "INCOMPATIBLE"
        and comparison.functional_relationship == "RELATED"
    ):
        return FDODecisionOutput(
            fdo_status="FDO",
            decision_reason=(
                "The declared data type matches the expected "
                "data type, but the declared purpose is "
                "incompatible with the expected functional purpose."
            ),
            decision_confidence=0.85,
        )

    # ---------------------------------------------------------
    # Rule 5: Different data type with extracted evidence
    # ---------------------------------------------------------
    if (
        comparison.data_match == "NO_MATCH"
        and comparison.functional_relationship == "RELATED"
    ):
        return FDODecisionOutput(
            fdo_status="FDO",
            decision_reason=(
                "The declared data type differs from the "
                "expected functional data type despite "
                "available evidence linking the collection "
                "to the evaluated function."
            ),
            decision_confidence=0.80,
        )

    # ---------------------------------------------------------
    # Conservative fallback
    # ---------------------------------------------------------
    return FDODecisionOutput(
        fdo_status="AMBIGUOUS",
        decision_reason=(
            "The available comparison evidence does not "
            "satisfy a deterministic FDO or NOT_FDO rule."
        ),
        decision_confidence=0.50,
    )