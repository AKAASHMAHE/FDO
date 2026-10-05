from pathlib import Path

from app.database import SessionLocal

from app.ontology.db_semantic_repository import (
    DBSemanticRepository,
)
from app.ontology.db_rdf_service import DBRDFService
from app.ontology.semantic_fuseki_service import (
    SemanticFusekiService,
)
from app.ontology.fuseki_decision_service import (
    FusekiDecisionService,
)


def test_real_db_semantic_finding_reaches_decision_engine(
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

        expected_data = repository.get_expected_mappings(
            application.application_id
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
            / "real-db-decision.ttl"
        )

        semantic_fuseki = SemanticFusekiService()

        semantic_fuseki.publish(
            graph,
            output_path,
        )

        decision_service = FusekiDecisionService()

        decisions = decision_service.evaluate()

        assert isinstance(decisions, list)

        for decision in decisions:
            assert decision.fdo_status in {
                "FDO",
                "NOT_FDO",
                "AMBIGUOUS",
            }

            assert decision.decision_reason

            if decision.decision_confidence is not None:
                assert (
                    0.0
                    <= decision.decision_confidence
                    <= 1.0
                )

    finally:
        session.close()