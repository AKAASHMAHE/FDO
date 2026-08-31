from app.database import SessionLocal

from app.services.analysis_service import create_analysis
from app.services.expected_mapping_service import get_expected_mapping
from app.services.evidence_service import get_evidence
from app.services.comparison_service import build_comparison
from app.services.comparison_persistence_service import save_comparison
from app.services.fdo_decision_service import (
    FDODecisionInput,
    evaluate_fdo_decision,
)
from app.services.result_service import save_fdo_result


def main():
    db = SessionLocal()

    try:
        application_id = "NAV-01"
        policy_id = "POL-NAV-01"
        expected_id = "EXP-099"
        evidence_id = "DEC-101"

        analysis_id = "ANALYSIS-NAV-01-TEST"
        comparison_id = "COMPARISON-EXP-099-DEC-101"

        # ---------------------------------------------------------
        # 1. Load real records
        # ---------------------------------------------------------
        expected = get_expected_mapping(
            db,
            expected_id,
        )

        evidence = get_evidence(
            db,
            evidence_id,
        )

        if not expected:
            raise ValueError(
                f"{expected_id} not found."
            )

        if not evidence:
            raise ValueError(
                f"{evidence_id} not found."
            )

        # ---------------------------------------------------------
        # 2. Create analysis
        # ---------------------------------------------------------
        analysis = create_analysis(
            db,
            analysis_id=analysis_id,
            application_id=application_id,
            policy_id=policy_id,
        )

        # ---------------------------------------------------------
        # 3. Build comparison
        # ---------------------------------------------------------
        comparison = build_comparison(
            expected,
            evidence,
        )

        # ---------------------------------------------------------
        # 4. Build decision input
        # ---------------------------------------------------------
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

        # ---------------------------------------------------------
        # 5. Persist comparison
        # ---------------------------------------------------------
        comparison_record = save_comparison(
            db,
            comparison_id=comparison_id,
            analysis_id=analysis.analysis_id,
            expected_id=expected.expected_id,
            evidence_id=evidence.evidence_id,
            comparison=comparison,
        )

        # ---------------------------------------------------------
        # 6. Persist FDO result
        # ---------------------------------------------------------
        result = save_fdo_result(
            db,
            comparison_id=comparison_record.comparison_id,
            decision=decision,
        )

        # ---------------------------------------------------------
        # 7. Commit
        # ---------------------------------------------------------
        db.commit()

        print("=== FDO PERSISTENCE TEST ===")
        print("Analysis ID:", analysis.analysis_id)
        print("Comparison ID:", comparison_record.comparison_id)
        print("Result ID:", result.result_id)
        print()

        print("FDO Status:", result.fdo_status)
        print("Confidence:", result.decision_confidence)
        print("Evidence:", comparison_record.evidence_id)
        print("Data Match:", comparison_record.data_match)
        print(
            "Purpose:",
            comparison_record.purpose_compatibility,
        )
        print(
            "Functional:",
            comparison_record.functional_relationship,
        )
        print(
            "Evidence Status:",
            comparison_record.evidence_status,
        )

        print()
        print("Persistence test committed successfully.")

    except Exception:
        db.rollback()
        print("Persistence test failed.")
        print("Transaction rolled back.")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()