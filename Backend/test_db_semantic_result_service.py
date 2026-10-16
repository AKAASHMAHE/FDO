from pathlib import Path

from app.database import SessionLocal

from app.ontology.db_semantic_repository import (
    DBSemanticRepository,
)
from app.ontology.db_semantic_result_service import (
    DBSemanticResultService,
)


def test_db_semantic_result_service_returns_unified_results(
    tmp_path,
):
    session = SessionLocal()

    try:
        repository = DBSemanticRepository(session)

        applications = repository.session.query(
            __import__(
                "app.models.application",
                fromlist=["Application"],
            ).Application
        ).all()

        if not applications:
            return

        application = applications[0]

        policies = repository.session.query(
            __import__(
                "app.models.policy_document",
                fromlist=["PolicyDocument"],
            ).PolicyDocument
        ).all()

        if not policies:
            return

        policy = policies[0]

        service = DBSemanticResultService(
            repository
        )

        results = service.analyze(
            application_id=(
                application.application_id
            ),
            policy_id=policy.policy_id,
            output_path=(
                Path(tmp_path)
                / "unified-semantic.ttl"
            ),
        )

        assert isinstance(results, list)

        for result in results:
            assert (
                result["application_id"]
                == application.application_id
            )

            assert result["application"]
            assert "function" in result
            assert result["expected_data"]
            assert "declared_data" in result

            assert result["expected_type"]
            assert "declared_type" in result

            assert result["expected_purpose"]
            assert "declared_purpose" in result

            assert result["fdo_status"] in {
                "FDO",
                "NOT_FDO",
                "AMBIGUOUS",
            }

            assert result["reason"]

            if result["confidence"] is not None:
                assert (
                    0.0
                    <= result["confidence"]
                    <= 1.0
                )

    finally:
        session.close()