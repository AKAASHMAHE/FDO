from __future__ import annotations

from .fdo_detection_queries import (
    COVERED_QUERY,
    FDO_DETECTION_QUERY,
    UNCOVERED_QUERY,
)
from .fuseki_service import FusekiService


class FusekiSemanticDetector:
    """
    Executes FDO semantic detection queries against Apache Jena Fuseki.
    """

    def __init__(
        self,
        service: FusekiService | None = None,
    ):
        self.service = service or FusekiService(
            dataset="fdo-reasoning"
        )

    def detect_fdo(self) -> list[dict]:
        """
        Execute the semantic FDO detection query against Fuseki.
        """

        return self._decode(self.service.query(FDO_DETECTION_QUERY))

    def detect_covered(self) -> list[dict]:
        return self._decode(self.service.query(COVERED_QUERY))

    def detect_uncovered(self) -> list[dict]:
        return self._decode(self.service.query(UNCOVERED_QUERY))

    @staticmethod
    def _decode(result: dict) -> list[dict]:
        return [
            {
                key: binding.get(variable, {}).get("value")
                for key, variable in {
                    "application": "application",
                    "application_id": "applicationId",
                    "function": "function",
                    "function_id": "functionId",
                    "function_name": "functionName",
                    "expected_data": "expectedData",
                    "expected_id": "expectedId",
                    "expected_type": "expectedType",
                    "expected_purpose": "expectedPurpose",
                    "expected_necessity": "expectedNecessity",
                    "expected_class": "expectedClass",
                    "declared_data": "declaredData",
                    "declared_id": "declaredId",
                    "declared_type": "declaredType",
                    "declared_class": "declaredClass",
                    "declared_purpose": "declaredPurpose",
                    "extraction_status": "extractionStatus",
                    "confidence": "confidence",
                    "evidence_text": "evidenceText",
                    "entity": "entity",
                    "type_relation": "typeRelation",
                }.items()
            }
            for binding in result["results"]["bindings"]
        ]