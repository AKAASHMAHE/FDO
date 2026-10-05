from __future__ import annotations

from pathlib import Path

from .db_rdf_service import DBRDFService
from .semantic_fuseki_service import SemanticFusekiService
from .fuseki_semantic_detector import FusekiSemanticDetector
from .semantic_decision_adapter import decide_semantic_finding


class DBSemanticAnalysisService:
    """
    Runs semantic FDO analysis starting from database-shaped records.
    """

    def __init__(
        self,
        db_rdf_service: DBRDFService | None = None,
        fuseki_service: SemanticFusekiService | None = None,
        detector: FusekiSemanticDetector | None = None,
    ):
        self.db_rdf_service = (
            db_rdf_service
            or DBRDFService()
        )

        self.fuseki_service = (
            fuseki_service
            or SemanticFusekiService()
        )

        self.detector = (
            detector
            or FusekiSemanticDetector(
                self.fuseki_service.fuseki_service
            )
        )

    def analyze(
        self,
        application,
        functions,
        expected_data,
        declared_data,
        output_path: str | Path,
    ) -> list[dict]:
        """
        Build RDF from DB records, publish it to Fuseki,
        detect semantic FDO findings, and evaluate them
        using the existing decision engine.
        """

        self.fuseki_service.fuseki_service.clear_default_graph()

        graph = self.db_rdf_service.build_graph(
            application=application,
            functions=functions,
            expected_data=expected_data,
            declared_data=declared_data,
        )

        self.fuseki_service.publish(
            graph,
            output_path,
        )

        findings = self.detector.detect_fdo()

        results = []

        for finding in findings:
            decision = decide_semantic_finding(
                finding
            )

            results.append(
                {
                    **finding,
                    "fdo_status": decision.fdo_status,
                    "confidence": (
                        decision.decision_confidence
                    ),
                    "reason": (
                        decision.decision_reason
                    ),
                }
            )

        return results