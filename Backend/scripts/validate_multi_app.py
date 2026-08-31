from app.database import SessionLocal
from app.services.analysis_runner import run_analysis


APPLICATIONS = [
    ("AMB-01", "ANALYSIS-AMB-01-VALIDATION"),
    ("EDU-02", "ANALYSIS-EDU-02-VALIDATION"),
    ("FIT-01", "ANALYSIS-FIT-01-VALIDATION"),
    ("FOD-01", "ANALYSIS-FOD-01-VALIDATION"),
]


def main():
    db = SessionLocal()

    try:
        print("=== MULTI-APPLICATION VALIDATION ===")

        for application_id, analysis_id in APPLICATIONS:

            print()
            print(
                f"--- {application_id} ---"
            )

            analysis = run_analysis(
                db,
                analysis_id,
                application_id,
            )

            db.commit()

            print(
                "Analysis:",
                analysis.analysis_id,
            )
            print(
                "Status:",
                analysis.analysis_status,
            )
            print(
                "Total:",
                analysis.total_mappings,
            )
            print(
                "FDO:",
                analysis.fdo_count,
            )
            print(
                "NOT_FDO:",
                analysis.not_fdo_count,
            )
            print(
                "AMBIGUOUS:",
                analysis.ambiguous_count,
            )

            valid = (
                analysis.total_mappings
                == (
                    analysis.fdo_count
                    + analysis.not_fdo_count
                    + analysis.ambiguous_count
                )
            )

            print(
                "Counter check:",
                valid,
            )

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()