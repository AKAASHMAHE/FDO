from __future__ import annotations

from .fdo_detection_queries import FDO_DETECTION_QUERY
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

        result = self.service.query(FDO_DETECTION_QUERY)

        findings = []

        for binding in result["results"]["bindings"]:
            findings.append(
                {
                    "expected_data": binding["expectedData"]["value"],
                    "declared_data": binding["declaredData"]["value"],
                    "expected_type": binding["expectedType"]["value"],
                    "declared_type": binding["declaredType"]["value"],
                    "expected_purpose": binding["expectedPurpose"]["value"],
                    "declared_purpose": binding["declaredPurpose"]["value"],
		    "application": binding["application"]["value"],
                    "function": binding["function"]["value"],
                }
            )

        return findings