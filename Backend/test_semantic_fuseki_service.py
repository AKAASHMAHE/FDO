from rdflib import Graph

from app.ontology.semantic_fuseki_service import (
    SemanticFusekiService,
)


class FakeFusekiService:

    def __init__(self):
        self.uploaded_path = None
        self.uploaded_content_type = None

    def upload_rdf(
        self,
        rdf_path,
        content_type="text/turtle",
    ):
        self.uploaded_path = str(rdf_path)
        self.uploaded_content_type = content_type


def test_semantic_fuseki_service_publishes_graph(
    tmp_path,
):
    graph = Graph()

    fake_fuseki = FakeFusekiService()

    service = SemanticFusekiService(
        fuseki_service=fake_fuseki,
    )

    output_path = (
        tmp_path / "semantic-test.ttl"
    )

    result = service.publish(
        graph,
        output_path,
    )

    assert result == output_path
    assert output_path.exists()

    assert (
        fake_fuseki.uploaded_path
        == str(output_path)
    )

    assert (
        fake_fuseki.uploaded_content_type
        == "text/turtle"
    )