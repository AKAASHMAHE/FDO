from __future__ import annotations

from .fuseki_semantic_detector import FusekiSemanticDetector
from .semantic_decision_adapter import decide_semantic_finding


class SemanticResultService:
    def __init__(self, detector: FusekiSemanticDetector | None = None):
        self.detector = detector or FusekiSemanticDetector()

    def analyze(self) -> list[dict]:
        findings = self.detector.detect_fdo()

        results = []

        for finding in findings:
            decision = decide_semantic_finding(finding)

            results.append(
                {
                    "application": finding.get("application"),
                    "function": finding.get("function"),
                    "expected_data": finding.get("expected_data"),
                    "declared_data": finding.get("declared_data"),
                    "expected_type": finding.get("expected_type"),
                    "declared_type": finding.get("declared_type"),
                    "expected_purpose": finding.get("expected_purpose"),
                    "declared_purpose": finding.get("declared_purpose"),
                    "fdo_status": decision.fdo_status,
                    "data_match_relation": decision.data_match_relation,
                    "confidence": decision.decision_confidence,
                    "reason": decision.decision_reason,
                }
            )

        return results