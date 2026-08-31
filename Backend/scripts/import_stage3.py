from pathlib import Path

import pandas as pd
from sqlalchemy.orm import Session

from app.database import engine
from app.models.application import Application
from app.models.function import Function
from app.models.expected_mapping import ExpectedMapping
from app.models.policy_document import PolicyDocument
from app.models.policy_evidence import PolicyEvidence


DATASET_PATH = Path(
    r"D:\VIT\PROJECT\TARP\DATA\FDO-Privacy_Final_Stage3_Dataset_CLEANED.xlsx"
)


def clean(value):
    """Convert pandas NaN values to None and normalize text."""
    if pd.isna(value):
        return None
    return str(value).strip()


def load_dataset():
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Stage 3 dataset not found: {DATASET_PATH}"
        )

    return {
        "applications": pd.read_excel(DATASET_PATH, "Applications"),
        "expected_data": pd.read_excel(DATASET_PATH, "Expected Data"),
        "policy_registry": pd.read_excel(DATASET_PATH, "Policy Registry"),
        "declared_data": pd.read_excel(DATASET_PATH, "Declared Data"),
    }


def import_dataset(data):
    applications = data["applications"]
    expected_data = data["expected_data"]
    policy_registry = data["policy_registry"]
    declared_data = data["declared_data"]

    with Session(engine) as session:
        try:
            # ---------------------------------------------------------
            # 1. Applications
            # ---------------------------------------------------------
            application_count = 0

            for _, row in applications.iterrows():
                app_id = clean(row["App ID"])

                existing = session.get(Application, app_id)

                if existing:
                    continue

                session.add(
                    Application(
                        application_id=app_id,
                        application_name=clean(row["Application"]),
                        category=clean(row["Category"]),
                        description=clean(row["Notes"]),
                    )
                )

                application_count += 1

            session.flush()

            # ---------------------------------------------------------
            # 2. Functions
            #
            # One function record = one App ID + Function ID pair.
            # This is necessary because Function IDs are reused
            # across applications in the Stage-3 dataset.
            # ---------------------------------------------------------
            function_count = 0

            functions = (
                expected_data[
                    [
                        "App ID",
                        "Function ID",
                        "Function",
                        "Feature",
                    ]
                ]
                .drop_duplicates(
                    subset=["App ID", "Function ID"]
                )
            )

            for _, row in functions.iterrows():
                app_id = clean(row["App ID"])
                function_id = clean(row["Function ID"])

                function_record_id = f"{app_id}:{function_id}"

                existing = session.get(
                    Function,
                    function_record_id,
                )

                if existing:
                    continue

                session.add(
                    Function(
                        function_record_id=function_record_id,
                        function_id=function_id,
                        application_id=app_id,
                        function_name=clean(row["Function"]),
                        feature=clean(row["Feature"]),
                        description=None,
                    )
                )

                function_count += 1

            session.flush()

            # ---------------------------------------------------------
            # 3. Expected Mappings
            # ---------------------------------------------------------
            expected_count = 0

            for _, row in expected_data.iterrows():
                expected_id = clean(row["Expected ID"])

                existing = session.get(
                    ExpectedMapping,
                    expected_id,
                )

                if existing:
                    continue

                app_id = clean(row["App ID"])
                function_id = clean(row["Function ID"])

                function_record_id = f"{app_id}:{function_id}"

                session.add(
                    ExpectedMapping(
                        expected_id=expected_id,
                        application_id=app_id,
                        function_record_id=function_record_id,
                        data_type=clean(row["Data Type"]),
                        necessity=clean(row["Necessity"]),
                        expected_purpose=clean(row["Purpose"]),
                        source_version=clean(row["Ontology Version"]),
                    )
                )

                expected_count += 1

            session.flush()

            # ---------------------------------------------------------
            # 4. Policy Documents
            # ---------------------------------------------------------
            policy_count = 0

            for _, row in policy_registry.iterrows():
                policy_id = clean(row["Policy ID"])

                existing = session.get(
                    PolicyDocument,
                    policy_id,
                )

                if existing:
                    continue

                app_id = clean(row["App ID"])

                source = clean(row["Policy URL/Source"])
                title = clean(row["Policy Title"])
                status = clean(row["Status"])

                document_name = title

                raw_text_parts = [
                    part
                    for part in [
                        source,
                        title,
                        status,
                        clean(row["Notes"]),
                    ]
                    if part
                ]

                raw_text = " | ".join(raw_text_parts)

                session.add(
                    PolicyDocument(
                        policy_id=policy_id,
                        application_id=app_id,
                        source_type=clean(row["Format"]),
                        source_identifier=source,
                        document_name=document_name,
                        raw_text=raw_text or "No policy text captured.",
                        retrieved_at=clean(row["Collection Date"]),
                        created_at=clean(row["Collection Date"]) or "",
                    )
                )

                policy_count += 1

            session.flush()

            # ---------------------------------------------------------
            # 5. Declared Data → Policy Evidence
            # ---------------------------------------------------------
            evidence_count = 0
            skipped_evidence = 0

            # App ID → Policy ID
            policy_by_app = {
                clean(row["App ID"]): clean(row["Policy ID"])
                for _, row in policy_registry.iterrows()
            }

            for _, row in declared_data.iterrows():
                evidence_id = clean(row["Declared ID"])
                app_id = clean(row["App ID"])

                policy_id = policy_by_app.get(app_id)

                # Never create orphan evidence.
                if not policy_id:
                    skipped_evidence += 1
                    print(
                        f"WARNING: No policy found for "
                        f"declared record {evidence_id} "
                        f"(App ID: {app_id})"
                    )
                    continue

                existing = session.get(
                    PolicyEvidence,
                    evidence_id,
                )

                if existing:
                    continue

                confidence_value = clean(row["Confidence"])

                # Keep confidence numeric where possible.
                confidence = None

                if confidence_value:
                    confidence_map = {
                        "high": 0.90,
                        "medium": 0.70,
                        "low": 0.40,
                    }

                    confidence = confidence_map.get(
                        confidence_value.lower()
                    )

                    if confidence is None:
                        try:
                            confidence = float(confidence_value)
                        except ValueError:
                            confidence = None

                session.add(
                    PolicyEvidence(
                        evidence_id=evidence_id,
                        policy_id=policy_id,
                        data_type=clean(
                            row["Normalized Data Type ID"]
                        ),
                        purpose=clean(row["Purpose"]),
                        entity=clean(row["Sharing/Recipient"]),
                        sharing=clean(row["Sharing/Recipient"]),
                        retention=clean(row["Retention"]),
                        evidence_text=clean(
                            row["Evidence Summary"]
                        )
                        or clean(row["Raw Policy Term"])
                        or "No evidence text captured.",
                        source_section=clean(row["Source Ref"]),
                        extraction_status=clean(row["Status"])
                        or "UNKNOWN",
                        confidence=confidence,
                    )
                )

                evidence_count += 1

            session.commit()

            print()
            print("=== FDO Stage 3 Import Complete ===")
            print(f"Applications inserted:    {application_count}")
            print(f"Functions inserted:       {function_count}")
            print(f"Expected mappings:        {expected_count}")
            print(f"Policy documents:         {policy_count}")
            print(f"Policy evidence:          {evidence_count}")
            print(f"Evidence skipped:         {skipped_evidence}")
            print()
            print("Database transaction committed successfully.")

        except Exception:
            session.rollback()
            print()
            print("ERROR: Import failed.")
            print("Database transaction rolled back.")
            raise


def main():
    print("=== FDO Stage 3 Database Import ===")
    print(f"Dataset: {DATASET_PATH}")
    print()

    data = load_dataset()
    import_dataset(data)


if __name__ == "__main__":
    main()