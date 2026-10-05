from __future__ import annotations


def build_semantic_explanation(result) -> str:
    """
    Build a deterministic, human-readable explanation
    from a persisted semantic FDO result.

    No new AI/LLM call is performed here.
    """

    status = result.fdo_status

    if status == "FDO":
        conclusion = (
            "Functional Data Overreach (FDO) was detected."
        )
    elif status == "NOT_FDO":
        conclusion = (
            "No Functional Data Overreach (FDO) was detected."
        )
    else:
        conclusion = (
            "The semantic analysis produced an ambiguous result."
        )

    explanation = (
        f"{conclusion} "
        f"The application function is '{result.function}'. "
        f"The expected data is '{result.expected_data}', "
        f"while the declared data is '{result.declared_data}'. "
        f"The expected purpose is '{result.expected_purpose}', "
        f"while the declared purpose is "
        f"'{result.declared_purpose}'. "
        f"Semantic decision reason: {result.reason}"
    )

    if result.confidence is not None:
        explanation += (
            f" Decision confidence: "
            f"{result.confidence:.2f}."
        )

    return explanation