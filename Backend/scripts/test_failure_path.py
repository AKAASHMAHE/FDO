from sqlalchemy import text

from app.database import SessionLocal
from app.services.analysis_runner import run_analysis


db = SessionLocal()
analysis_id = "ANALYSIS-INVALID-TEST"

try:
    print("=== FAILURE PATH TEST ===")

    try:
        run_analysis(
            db,
            analysis_id,
            "INVALID-APP",
        )

        print("ERROR: analysis unexpectedly succeeded")

    except Exception as e:
        db.rollback()

        print(
            "Expected failure:",
            type(e).__name__,
        )

        print(
            "Message:",
            str(e),
        )

    exists = db.execute(
        text(
            "SELECT COUNT(*) "
            "FROM analyses "
            "WHERE analysis_id=:aid"
        ),
        {"aid": analysis_id},
    ).scalar()

    print(
        "Analysis records after failure:",
        exists,
    )

finally:
    db.close()
    