from app.database import SessionLocal
from app.ontology.db_rdf_service import DBRDFService
from app.ontology.db_semantic_repository import (
    DBSemanticRepository,
)


def test_real_policy_evidence_builds_declared_data_rdf():

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

        policies = session.query(
            __import__(
                "app.models.policy_document",
                fromlist=["PolicyDocument"],
            ).PolicyDocument
        ).all()

        if not policies:
            return

        policy = policies[0]

        evidence = repository.get_policy_evidence(
            policy.policy_id
        )

        rdf_service = DBRDFService()

        graph = rdf_service.build_graph(
            application=application,
            functions=repository.get_functions(
                application.application_id
            ),
            expected_data=repository.get_expected_mappings(
                application.application_id
            ),
            declared_data=evidence,
        )

        assert len(graph) > 0

        if evidence:
            evidence_id = evidence[0].evidence_id

            declared_uri = (
                "http://example.org/fdo#resource/"
                f"declared-data/{evidence_id}"
            )

            assert any(
                str(subject) == declared_uri
                for subject in graph.subjects()
            )

    finally:
        session.close()