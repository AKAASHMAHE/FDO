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
    data_match_relation: str = "NONE"
    is_uncovered_declaration: bool = False


@dataclass
class FDODecisionOutput:
    fdo_status: str
    decision_reason: str
    decision_confidence: float | None
    data_match_relation: str = "NONE"
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

    if comparison.data_match == "ANCILLARY":
        return FDODecisionOutput(
            fdo_status="NOT_FDO",
            decision_reason=(
                "This declaration is covered by the cross-application "
                "ancillary baseline."
            ),
            decision_confidence=0.75,
            data_match_relation=comparison.data_match_relation,
        )

    if comparison.is_uncovered_declaration:
        if comparison.purpose_compatibility == "INCOMPATIBLE":
            return FDODecisionOutput(
                fdo_status="FDO",
                decision_reason=(
                    "Declared data is not in the functional baseline, "
                    "and its purpose is incompatible with every expected "
                    "purpose for the application."
                ),
                decision_confidence=0.80,
                data_match_relation=comparison.data_match_relation,
            )
        if comparison.purpose_compatibility == "COMPATIBLE":
            return FDODecisionOutput(
                fdo_status="AMBIGUOUS",
                decision_reason=(
                    "declared data not in the functional baseline; purpose "
                    "is compatible, possible baseline gap"
                ),
                decision_confidence=0.50,
                data_match_relation=comparison.data_match_relation,
            )
        return FDODecisionOutput(
            fdo_status="AMBIGUOUS",
            decision_reason=(
                "Uncovered declaration has an unknown purpose; "
                "its relationship to the functional baseline cannot be determined."
            ),
            decision_confidence=0.40,
            data_match_relation=comparison.data_match_relation,
        )

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
            data_match_relation=comparison.data_match_relation,
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
            data_match_relation=comparison.data_match_relation,
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
            data_match_relation=comparison.data_match_relation,
        )

    if comparison.purpose_compatibility == "UNKNOWN":
        return FDODecisionOutput(
            fdo_status="AMBIGUOUS",
            decision_reason=(
                "The declared or expected purpose is unclassified, "
                "so purpose compatibility cannot be determined."
            ),
            decision_confidence=0.40,
            data_match_relation=comparison.data_match_relation,
        )

    if comparison.data_match == "EXACT_MATCH":
        match_description = "matched via exact type"
    elif comparison.data_match_relation == "BROADER_EVIDENCE":
        match_description = "matched via broader type"
    elif comparison.data_match_relation == "NARROWER_EVIDENCE":
        match_description = "matched via narrower type"
    else:
        match_description = "did not match by type"

    # ---------------------------------------------------------
    # Rule 3: Matching data + compatible purpose + related
    # ---------------------------------------------------------
    if (
        comparison.data_match in {
            "EXACT_MATCH",
            "HIERARCHICAL_MATCH",
        }
        and comparison.purpose_compatibility == "COMPATIBLE"
        and comparison.functional_relationship == "RELATED"
    ):
        return FDODecisionOutput(
            fdo_status="NOT_FDO",
            decision_reason=(
                "The declared data type matches the expected "
                "data type, the declared purpose is compatible "
                "with the expected purpose, and evidence is "
                f"{match_description} for the function."
            ),
            decision_confidence=(
                0.75
                if comparison.data_match_relation == "BROADER_EVIDENCE"
                else 0.90
            ),
            data_match_relation=comparison.data_match_relation,
        )

    # ---------------------------------------------------------
    # Rule 4: Matching data + incompatible purpose + related
    # ---------------------------------------------------------
    if (
        comparison.data_match in {
            "EXACT_MATCH",
            "HIERARCHICAL_MATCH",
        }
        and comparison.purpose_compatibility == "INCOMPATIBLE"
        and comparison.functional_relationship == "RELATED"
    ):
        return FDODecisionOutput(
            fdo_status="FDO",
            decision_reason=(
                "The declared data type matches the expected "
                "data type, but the declared purpose is "
                "incompatible with the expected functional purpose "
                f"({match_description})."
            ),
            decision_confidence=0.85,
            data_match_relation=comparison.data_match_relation,
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
            data_match_relation=comparison.data_match_relation,
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
        data_match_relation=comparison.data_match_relation,
    )