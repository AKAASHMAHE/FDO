from dataclasses import dataclass


@dataclass
class ComparisonInput:
    expected_id: str
    application_id: str
    function_record_id: str
    expected_data_type: str
    expected_necessity: str
    expected_purpose: str

    declared_evidence_id: str | None
    declared_data_type: str | None
    declared_purpose: str | None
    declared_sharing: str | None
    declared_retention: str | None


@dataclass
class ComparisonOutput:
    expected_id: str
    declared_evidence_id: str | None

    data_match: str
    purpose_compatibility: str
    functional_relationship: str
    functional_justification: str
    evidence_status: str


def build_comparison_input(
    expected,
    evidence=None,
) -> ComparisonInput:
    return ComparisonInput(
        expected_id=expected.expected_id,
        application_id=expected.application_id,
        function_record_id=expected.function_record_id,
        expected_data_type=expected.data_type,
        expected_necessity=expected.necessity,
        expected_purpose=expected.expected_purpose,
        declared_evidence_id=(
            evidence.evidence_id if evidence else None
        ),
        declared_data_type=(
            evidence.data_type if evidence else None
        ),
        declared_purpose=(
            evidence.purpose if evidence else None
        ),
        declared_sharing=(
            evidence.sharing if evidence else None
        ),
        declared_retention=(
            evidence.retention if evidence else None
        ),
    )
def evaluate_data_match(
    expected_data_type: str,
    declared_data_type: str | None,
) -> str:
    """
    Compare the expected normalized data type with
    the declared normalized data type.

    Returns:
        EXACT_MATCH
        NO_MATCH
        NO_EVIDENCE
    """

    if not declared_data_type:
        return "NO_EVIDENCE"

    if expected_data_type == declared_data_type:
        return "EXACT_MATCH"

    return "NO_MATCH"
def evaluate_purpose_compatibility(
    expected_purpose: str,
    declared_purpose: str | None,
) -> str:
    """
    Evaluate whether the declared purpose is compatible
    with the expected purpose.

    This is the deterministic baseline.
    Semantic/AI evaluation will be added later.

    Returns:
        COMPATIBLE
        INCOMPATIBLE
        NO_EVIDENCE
    """

    if not declared_purpose:
        return "NO_EVIDENCE"

    expected = expected_purpose.strip().lower()
    declared = declared_purpose.strip().lower()

    if not expected or not declared:
        return "NO_EVIDENCE"

    if expected == declared:
        return "COMPATIBLE"

    return "INCOMPATIBLE"

def evaluate_functional_relationship(
    declared_evidence_id: str | None,
) -> str:
    """
    Determine whether declared evidence is available for
    functional relationship analysis.

    This is only an evidence-presence baseline.
    It does not make the final FDO decision.

    Returns:
        RELATED
        NO_EVIDENCE
    """

    if not declared_evidence_id:
        return "NO_EVIDENCE"

    return "RELATED"
def evaluate_evidence_status(
    declared_evidence_id: str | None,
    extraction_status: str | None,
) -> str:
    """
    Classify the availability and extraction state of
    declared evidence.

    Returns:
        NO_EVIDENCE
        EXTRACTED
        INSUFFICIENT
        UNKNOWN
    """

    if not declared_evidence_id:
        return "NO_EVIDENCE"

    if not extraction_status:
        return "UNKNOWN"

    status = extraction_status.strip().upper()

    if status == "EXTRACTED":
        return "EXTRACTED"

    if status == "INSUFFICIENT":
        return "INSUFFICIENT"

    return "UNKNOWN"
def build_comparison(
    expected,
    evidence=None,
) -> ComparisonOutput:
    """
    Build a deterministic comparison result from an
    expected mapping and optional declared evidence.

    This function does NOT make the final FDO decision.
    """

    data_match = evaluate_data_match(
        expected.data_type,
        evidence.data_type if evidence else None,
    )

    purpose_compatibility = evaluate_purpose_compatibility(
        expected.expected_purpose,
        evidence.purpose if evidence else None,
    )

    functional_relationship = evaluate_functional_relationship(
        evidence.evidence_id if evidence else None,
    )

    evidence_status = evaluate_evidence_status(
        evidence.evidence_id if evidence else None,
        evidence.extraction_status if evidence else None,
    )

    if not evidence:
        justification = (
            "No declared evidence is available for comparison."
        )
    else:
        justification = (
            "Declared evidence is available for "
            "data, purpose, and functional analysis."
        )

    return ComparisonOutput(
        expected_id=expected.expected_id,
        declared_evidence_id=(
            evidence.evidence_id if evidence else None
        ),
        data_match=data_match,
        purpose_compatibility=purpose_compatibility,
        functional_relationship=functional_relationship,
        functional_justification=justification,
        evidence_status=evidence_status,
    )