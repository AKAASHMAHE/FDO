from app.database import SessionLocal

from app.services.expected_mapping_service import (
    get_expected_mapping,
)

from app.services.evidence_service import (
    get_evidence,
)

from app.services.comparison_service import (
    build_comparison,
)

from app.services.fdo_decision_service import (
    FDODecisionInput,
    evaluate_fdo_decision,
)


def main():
    db = SessionLocal()

    try:
        expected = get_expected_mapping(
            db,
            "EXP-099",
        )

        evidence = get_evidence(
            db,
            "DEC-101",
        )

        if not expected:
            raise ValueError("EXP-099 not found.")

        if not evidence:
            raise ValueError("DEC-101 not found.")

        comparison = build_comparison(
            expected,
            evidence,
        )

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
            purpose_compatibility=(
                comparison.purpose_compatibility
            ),
            functional_relationship=(
                comparison.functional_relationship
            ),
            evidence_status=comparison.evidence_status,
        )

        decision = evaluate_fdo_decision(
            decision_input
        )

        print("=== REAL FDO DECISION TEST ===")
        print(
            "Expected:",
            expected.expected_id,
            expected.data_type,
        )
        print(
            "Declared:",
            evidence.evidence_id,
            evidence.data_type,
        )
        print()

        print("Data match:")
        print(comparison.data_match)

        print("Purpose compatibility:")
        print(comparison.purpose_compatibility)

        print("Functional relationship:")
        print(comparison.functional_relationship)

        print("Evidence status:")
        print(comparison.evidence_status)

        print()

        print("=== FDO DECISION ===")
        print("Status:", decision.fdo_status)
        print("Reason:", decision.decision_reason)
        print("Confidence:", decision.decision_confidence)

    finally:
        db.close()


if __name__ == "__main__":
    main()