from __future__ import annotations

from .semantic_result_service import SemanticResultService


class SemanticAnalysisService:
    """
    Orchestrates semantic FDO analysis using the RDF/Fuseki layer.
    """

    def __init__(
        self,
        result_service: SemanticResultService | None = None,
    ):
        self.result_service = result_service or SemanticResultService()

    def analyze(self) -> list[dict]:
        return self.result_service.analyze()