from app.database import SessionLocal
from app.ontology.db_rdf_service import DBRDFService
from app.ontology.db_semantic_repository import (
    DBSemanticRepository,
)


def test_real_orm_records_build_rdf_graph():

    session = SessionLocal()

    try:
        repository = DBSemanticRepository(session)

        applications = session.query(
            __import__(
                "app.models.application",
                fromlist=["Application"],
            ).Application
        ).all()

        if not applications:
            return

        application = applications[0]

        functions = repository.get_functions(
            application.application_id
        )

        expected_data = repository.get_expected_mappings(
            application.application_id
        )

        rdf_service = DBRDFService()

        graph = rdf_service.build_graph(
            application=application,
            functions=functions,
            expected_data=expected_data,
            declared_data=[],
        )

        assert len(graph) > 0

        application_uri = (
            "http://example.org/fdo#resource/"
            f"application/{application.application_id}"
        )

        assert any(
            str(subject) == application_uri
            for subject in graph.subjects()
        )

    finally:
        session.close()