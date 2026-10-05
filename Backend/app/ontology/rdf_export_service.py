"""
RDF graph export service.

Provides a stable interface for serializing the semantic FDO graph
for persistence and external RDF/SPARQL stores.
"""

from pathlib import Path

from rdflib import Graph


def export_rdf_graph(
    graph: Graph,
    output_path: str | Path,
    format: str = "turtle",
) -> Path:
    """
    Serialize an RDF graph to disk.

    Args:
        graph: RDFLib graph containing FDO semantic instances.
        output_path: Destination file.
        format: RDF serialization format.

    Returns:
        Path to the generated RDF file.
    """

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    graph.serialize(
        destination=str(path),
        format=format,
    )

    return path