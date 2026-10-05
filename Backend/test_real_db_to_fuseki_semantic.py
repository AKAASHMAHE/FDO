from pathlib import Path

from app.database import SessionLocal
from app.ontology.db_semantic_repository import (
    DBSemanticRepository,
)
from app.ontology.db_rdf_service import DBRDFService
from app.ontology.semantic_fuseki_service import (
    SemanticFusekiService,
)
from app.ontology.fuseki_semantic_detector import (
    FusekiSemanticDetector,
)


def test_real_db_to_fuseki_semantic_detection(
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

        functions = repository.get_functions(
            application.application_id
        )

        expected_data = (
            repository.get_expected_mappings(
                application.application_id
            )
        )

        policies = repository.session.query(
            __import__(
                "app.models.policy_document",
                fromlist=["PolicyDocument"],
            ).PolicyDocument
        ).all()

        if not policies:
            return

        policy = policies[0]

        declared_data = (
            repository.get_policy_evidence(
                policy.policy_id
            )
        )

        rdf_service = DBRDFService()

        graph = rdf_service.build_graph(
            application=application,
            functions=functions,
            expected_data=expected_data,
            declared_data=declared_data,
        )

        assert len(graph) > 0

        output_path = (
            Path(tmp_path)
            / "real-db-semantic.ttl"
        )

        fuseki_service = SemanticFusekiService()

        fuseki_service.publish(
            graph,
            output_path,
        )

        detector = FusekiSemanticDetector(
            fuseki_service.fuseki_service
        )

        findings = detector.detect_fdo()

        assert isinstance(findings, list)

        application_uri = (
            "http://example.org/fdo#resource/"
            f"application/{application.application_id}"
        )

        application_findings = [
            finding
            for finding in findings
            if finding["application"]
            == application_uri
        ]

        assert isinstance(
            application_findings,
            list,
        )

    finally:
        session.close()