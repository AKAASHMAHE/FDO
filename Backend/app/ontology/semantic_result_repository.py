from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.semantic_fdo_result import SemanticFDOResult


class SemanticResultRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_results(
        self,
        analysis_id: str,
        results: list[dict],
    ) -> list[SemanticFDOResult]:
        saved_results = []

        for index, result in enumerate(results, start=1):
            semantic_result_id = (
                f"{analysis_id}:SEMANTIC:{index:03d}"
            )

            entity = SemanticFDOResult(
                semantic_result_id=semantic_result_id,
                analysis_id=analysis_id,
                application_id=result["application_id"],
                application=result["application"],
                function=result["function"],
                expected_data=result["expected_data"],
                declared_data=result["declared_data"],
                expected_type=result["expected_type"],
                declared_type=result["declared_type"],
                expected_purpose=result["expected_purpose"],
                declared_purpose=result["declared_purpose"],
                fdo_status=result["fdo_status"],
                confidence=result["confidence"],
                reason=result["reason"],
                created_at=datetime.now(timezone.utc).isoformat(),
            )

            self.db.add(entity)
            saved_results.append(entity)

        self.db.flush()

        return saved_results

    def get_by_analysis_id(
        self,
        analysis_id: str,
    ) -> list[SemanticFDOResult]:
        return (
            self.db.query(SemanticFDOResult)
            .filter(
                SemanticFDOResult.analysis_id == analysis_id
            )
            .order_by(
                SemanticFDOResult.semantic_result_id
            )
            .all()
        )