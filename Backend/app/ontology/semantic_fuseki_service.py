from __future__ import annotations

from pathlib import Path

from rdflib import Graph

from .fuseki_service import FusekiService


class SemanticFusekiService:
    """
    Publishes an RDF graph to the FDO Fuseki dataset.
    """

    def __init__(
        self,
        fuseki_service: FusekiService | None = None,
    ):
        self.fuseki_service = (
            fuseki_service
            or FusekiService(dataset="fdo-reasoning")
        )

    def publish(
        self,
        graph: Graph,
        output_path: str | Path,
    ) -> Path:
        """
        Serialize an RDF graph and upload it to Fuseki.
        """

        path = Path(output_path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        graph.serialize(
            destination=str(path),
            format="turtle",
        )

        self.fuseki_service.upload_rdf(
            path,
            content_type="text/turtle",
        )

        return path