from pathlib import Path

from rdflib import Graph

from app.ontology.rdf_export_service import export_rdf_graph
from app.ontology.rdf_instance_builder import build_rdf_graph


def test_export_rdf_graph_creates_turtle_file(tmp_path: Path):
    graph = build_rdf_graph(
        applications=[
            {
                "id": "whatsapp",
                "name": "WhatsApp",
            }
        ],
        functions=[
            {
                "id": "messaging",
                "name": "Messaging",
            }
        ],
    )

    output_path = tmp_path / "fdo_graph.ttl"

    result = export_rdf_graph(
        graph,
        output_path,
    )

    assert result == output_path
    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_exported_rdf_can_be_loaded_again(tmp_path: Path):
    graph = build_rdf_graph(
        applications=[
            {
                "id": "whatsapp",
                "name": "WhatsApp",
            }
        ]
    )

    output_path = tmp_path / "fdo_graph.ttl"

    export_rdf_graph(
        graph,
        output_path,
    )

    loaded_graph = Graph()
    loaded_graph.parse(
        output_path,
        format="turtle",
    )

    assert len(loaded_graph) == len(graph)


def test_export_supports_xml_format(tmp_path: Path):
    graph = build_rdf_graph(
        applications=[
            {
                "id": "whatsapp",
                "name": "WhatsApp",
            }
        ]
    )

    output_path = tmp_path / "fdo_graph.rdf"

    export_rdf_graph(
        graph,
        output_path,
        format="xml",
    )

    assert output_path.exists()
    assert output_path.stat().st_size > 0