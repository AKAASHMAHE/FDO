from app.database import SessionLocal
from app.models.semantic_fdo_result import SemanticFDOResult
from app.ontology.semantic_result_repository import SemanticResultRepository


def test_semantic_result_repository_save_and_get():
    db = SessionLocal()

    analysis_id = "TEST-SEMANTIC-PERSISTENCE"

    try:
        repository = SemanticResultRepository(db)

        results = [
            {
                "application_id": "NAV-01",
                "application": "Google Maps",
                "function": "Turn-by-turn navigation",
                "expected_data": "DATA.LOCATION.PRECISE",
                "declared_data": "DATA.LOCATION.PRECISE",
                "expected_type": "DATA.LOCATION.PRECISE",
                "declared_type": "DATA.LOCATION.PRECISE",
                "expected_purpose": "Route/navigation",
                "declared_purpose": "Route/navigation",
                "fdo_status": "NOT_FDO",
                "confidence": 0.95,
                "reason": "Test semantic persistence.",
            }
        ]

        saved = repository.save_results(
            analysis_id=analysis_id,
            results=results,
        )

        db.commit()

        assert len(saved) == 1
        assert saved[0].analysis_id == analysis_id
        assert saved[0].application_id == "NAV-01"

        loaded = repository.get_by_analysis_id(
            analysis_id
        )

        assert len(loaded) == 1
        assert loaded[0].semantic_result_id == (
            f"{analysis_id}:SEMANTIC:001"
        )
        assert loaded[0].application == "Google Maps"
        assert loaded[0].function == "Turn-by-turn navigation"
        assert loaded[0].fdo_status == "NOT_FDO"
        assert loaded[0].confidence == 0.95

    finally:
        db.query(SemanticFDOResult).filter(
            SemanticFDOResult.analysis_id == analysis_id
        ).delete(
            synchronize_session=False
        )
        db.commit()
        db.close()