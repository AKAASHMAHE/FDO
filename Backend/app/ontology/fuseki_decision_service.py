from __future__ import annotations

from app.services.fdo_decision_service import (
    FDODecisionOutput,
)

from .fuseki_semantic_detector import FusekiSemanticDetector
from .semantic_decision_adapter import decide_semantic_finding


class FusekiDecisionService:
    """
    Runs semantic FDO detection through Fuseki and evaluates
    each semantic finding using the existing FDO decision engine.
    """

    def __init__(self, detector: FusekiSemanticDetector | None = None):
        self.detector = detector or FusekiSemanticDetector()

    def evaluate(self) -> list[FDODecisionOutput]:
        findings = self.detector.detect_fdo()

        decisions = []

        for finding in findings:
            decision = decide_semantic_finding(finding)
            decisions.append(decision)

        return decisions