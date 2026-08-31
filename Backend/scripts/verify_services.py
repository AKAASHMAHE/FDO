from app.database import SessionLocal

from app.services.application_service import (
    get_application,
)

from app.services.function_service import (
    get_functions_by_application,
)

from app.services.expected_mapping_service import (
    get_expected_mappings_by_application,
)

from app.services.policy_service import (
    get_policy_documents_by_application,
)

from app.services.evidence_service import (
    get_evidence_by_policy,
)


def main():
    db = SessionLocal()

    try:
        application_id = "COM-01"

        print("=== FDO Service Integration Verification ===")
        print(f"Application: {application_id}")
        print()

        # 1. Application
        application = get_application(
            db,
            application_id,
        )

        print(
            "Application:",
            application.application_name
            if application
            else None,
        )

        # 2. Functions
        functions = get_functions_by_application(
            db,
            application_id,
        )

        print(
            "Functions:",
            len(functions),
        )

        # 3. Expected mappings
        expected = get_expected_mappings_by_application(
            db,
            application_id,
        )

        print(
            "Expected mappings:",
            len(expected),
        )

        # 4. Policy
        policies = get_policy_documents_by_application(
            db,
            application_id,
        )

        print(
            "Policy documents:",
            len(policies),
        )

        # 5. Evidence
        evidence_count = 0

        for policy in policies:
            evidence = get_evidence_by_policy(
                db,
                policy.policy_id,
            )

            evidence_count += len(evidence)

        print(
            "Policy evidence:",
            evidence_count,
        )

        print()
        print("=== Integration Summary ===")

        print(
            "Application loaded:",
            application is not None,
        )

        print(
            "Functions loaded:",
            len(functions),
        )

        print(
            "Expected mappings loaded:",
            len(expected),
        )

        print(
            "Policies loaded:",
            len(policies),
        )

        print(
            "Evidence loaded:",
            evidence_count,
        )

        print()
        print("Service integration verification complete.")

    finally:
        db.close()


if __name__ == "__main__":
    main()