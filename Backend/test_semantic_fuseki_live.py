from rdflib import Graph, Literal, RDF

from app.ontology.namespace import FDO
from app.ontology.semantic_fuseki_service import (
    SemanticFusekiService,
)


def test_semantic_fuseki_service_uploads_to_real_fuseki(
    tmp_path,
):
    graph = Graph()

    subject = FDO["resource/test/live-001"]

    graph.add(
        (
            subject,
            RDF.type,
            FDO.ExpectedData,
        )
    )

    graph.add(
        (
            subject,
            FDO.id,
            Literal("live-001"),
        )
    )

    output_path = (
        tmp_path / "live-fuseki-test.ttl"
    )

    service = SemanticFusekiService()

    result = service.publish(
        graph,
        output_path,
    )

    assert result == output_path
    assert output_path.exists()

    query = """
    PREFIX fdo: <http://example.org/fdo#>

    SELECT ?id
    WHERE {
        ?subject a fdo:ExpectedData ;
                 fdo:id ?id .
        FILTER(?id = "live-001")
    }
    """

    response = service.fuseki_service.query(
        query
    )

    bindings = response["results"]["bindings"]

    assert len(bindings) >= 1
    assert bindings[0]["id"]["value"] == "live-001"