from __future__ import annotations

from pathlib import Path

from .db_semantic_repository import DBSemanticRepository
from .db_rdf_service import DBRDFService
from .semantic_fuseki_service import SemanticFusekiService
from .fuseki_semantic_detector import FusekiSemanticDetector
from .semantic_decision_adapter import decide_semantic_finding


class DBSemanticResultService:
    """
    Runs semantic FDO analysis from real database records
    and returns unified structured results.
    """

    def __init__(
        self,
        repository: DBSemanticRepository,
        db_rdf_service: DBRDFService | None = None,
        fuseki_service: SemanticFusekiService | None = None,
    ):
        self.repository = repository

        self.db_rdf_service = (
            db_rdf_service
            or DBRDFService()
        )

        self.fuseki_service = (
            fuseki_service
            or SemanticFusekiService()
        )

    def analyze(
        self,
        application_id: str,
        policy_id: str,
        output_path: str | Path,
    ) -> list[dict]:

        application = self.repository.get_application(
            application_id
        )

        functions = self.repository.get_functions(
            application_id
        )

        expected_data = (
            self.repository.get_expected_mappings(
                application_id
            )
        )

        declared_data = (
            self.repository.get_policy_evidence(
                policy_id
            )
        )

        # ---------------------------------------------------------
        # Clear previous semantic analysis data
        # ---------------------------------------------------------

        self.fuseki_service.fuseki_service.clear_default_graph()

        # ---------------------------------------------------------
        # Build RDF graph from current DB records
        # ---------------------------------------------------------

        graph = self.db_rdf_service.build_graph(
            application=application,
            functions=functions,
            expected_data=expected_data,
            declared_data=declared_data,
        )

        # ---------------------------------------------------------
        # Publish current analysis graph to Fuseki
        # ---------------------------------------------------------

        self.fuseki_service.publish(
            graph,
            output_path,
        )

        # ---------------------------------------------------------
        # Detect semantic FDO findings
        # ---------------------------------------------------------

        detector = FusekiSemanticDetector(
            self.fuseki_service.fuseki_service
        )

        findings = detector.detect_fdo()

        results = []

        for finding in findings:

            if not finding["application"].endswith(
                f"/application/{application_id}"
            ):
                continue

            decision = decide_semantic_finding(
                finding
            )

            results.append(
                {
                    "application_id": application_id,
                    "application": finding["application"],
                    "function": finding["function"],
                    "expected_data": finding["expected_data"],
                    "declared_data": finding["declared_data"],
                    "expected_type": finding["expected_type"],
                    "declared_type": finding["declared_type"],
                    "expected_purpose": finding["expected_purpose"],
                    "declared_purpose": finding["declared_purpose"],
                    "fdo_status": decision.fdo_status,
                    "confidence": decision.decision_confidence,
                    "reason": decision.decision_reason,
                }
            )

        return results