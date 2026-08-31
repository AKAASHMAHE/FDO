from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.analysis import Analysis

from app.services.application_service import (
    get_application,
)

from app.services.expected_mapping_service import (
    get_expected_mappings_by_application,
)

from app.services.policy_service import (
    get_policy_documents_by_application,
)

from app.services.comparison_service import (
    build_comparison,
)

from app.services.comparison_persistence_service import (
    save_comparison,
)

from app.services.fdo_decision_service import (
    FDODecisionInput,
    evaluate_fdo_decision,
)

from app.services.result_service import (
    save_fdo_result,
)

from app.services.evidence_matcher import (
    find_matching_evidence,
)


def run_analysis(
    session: Session,
    analysis_id: str,
    application_id: str,
) -> Analysis:

    existing = session.get(
        Analysis,
        analysis_id,
    )

    if existing:
        raise ValueError(
            f"Analysis already exists: {analysis_id}"
        )

    try:
        # ---------------------------------------------------------
        # 1. Load application
        # ---------------------------------------------------------

        application = get_application(
            session,
            application_id,
        )

        if not application:
            raise ValueError(
                f"Application not found: {application_id}"
            )

        # ---------------------------------------------------------
        # 2. Load policy
        # ---------------------------------------------------------

        policies = get_policy_documents_by_application(
            session,
            application_id,
        )

        if not policies:
            raise ValueError(
                f"No policy document found for: {application_id}"
            )

        policy = policies[0]

        # ---------------------------------------------------------
        # 3. Create analysis
        # ---------------------------------------------------------

        analysis = Analysis(
            analysis_id=analysis_id,
            application_id=application_id,
            policy_id=policy.policy_id,
            analysis_status="RUNNING",
            total_mappings=0,
            fdo_count=0,
            not_fdo_count=0,
            ambiguous_count=0,
            created_at=datetime.now(
                timezone.utc
            ).isoformat(),
        )

        session.add(analysis)
        session.flush()

        # ---------------------------------------------------------
        # 4. Load expected mappings
        # ---------------------------------------------------------

        expected_mappings = (
            get_expected_mappings_by_application(
                session,
                application_id,
            )
        )

        # ---------------------------------------------------------
        # 5. Process mappings
        # ---------------------------------------------------------

        for expected in expected_mappings:

            matching_evidence = find_matching_evidence(
                session,
                policy.policy_id,
                expected.data_type,
            )

            comparison = build_comparison(
                expected,
                matching_evidence,
            )

            decision_input = FDODecisionInput(
                expected_id=expected.expected_id,
                application_id=expected.application_id,
                expected_data_type=expected.data_type,
                expected_necessity=expected.necessity,
                expected_purpose=expected.expected_purpose,
                declared_evidence_id=(
                    matching_evidence.evidence_id
                    if matching_evidence
                    else None
                ),
                declared_data_type=(
                    matching_evidence.data_type
                    if matching_evidence
                    else None
                ),
                declared_purpose=(
                    matching_evidence.purpose
                    if matching_evidence
                    else None
                ),
                data_match=comparison.data_match,
                purpose_compatibility=(
                    comparison.purpose_compatibility
                ),
                functional_relationship=(
                    comparison.functional_relationship
                ),
                evidence_status=(
                    comparison.evidence_status
                ),
            )

            decision = evaluate_fdo_decision(
                decision_input
            )

            comparison_id = (
                f"{analysis_id}:{expected.expected_id}"
            )

            comparison_record = save_comparison(
                session,
                comparison_id=comparison_id,
                analysis_id=analysis.analysis_id,
                expected_id=expected.expected_id,
                evidence_id=(
                    matching_evidence.evidence_id
                    if matching_evidence
                    else None
                ),
                comparison=comparison,
            )

            save_fdo_result(
                session,
                comparison_id=(
                    comparison_record.comparison_id
                ),
                decision=decision,
            )

            analysis.total_mappings += 1

            if decision.fdo_status == "FDO":
                analysis.fdo_count += 1

            elif decision.fdo_status == "NOT_FDO":
                analysis.not_fdo_count += 1

            else:
                analysis.ambiguous_count += 1

        # ---------------------------------------------------------
        # 6. Validate counters
        # ---------------------------------------------------------

        classified = (
            analysis.fdo_count
            + analysis.not_fdo_count
            + analysis.ambiguous_count
        )

        if classified != analysis.total_mappings:
            raise ValueError(
                "Analysis counter mismatch: "
                f"{classified} classified vs "
                f"{analysis.total_mappings} total."
            )

        # ---------------------------------------------------------
        # 7. Complete analysis
        # ---------------------------------------------------------

        analysis.analysis_status = "COMPLETED"

        session.flush()

        return analysis

    except Exception:
        session.rollback()
        raise