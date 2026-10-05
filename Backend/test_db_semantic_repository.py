from app.database import SessionLocal
from app.ontology.db_semantic_repository import (
    DBSemanticRepository,
)


def test_db_semantic_repository_reads_real_database():

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

        loaded = repository.get_application(
            application.application_id
        )

        assert (
            loaded.application_id
            == application.application_id
        )

        functions = repository.get_functions(
            application.application_id
        )

        expected = repository.get_expected_mappings(
            application.application_id
        )

        assert isinstance(functions, list)
        assert isinstance(expected, list)

    finally:
        session.close()