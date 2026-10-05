from app.ontology.fuseki_service import FusekiService


def test_fuseki_default_graph_can_be_cleared():

    service = FusekiService(
        dataset="fdo-reasoning"
    )

    service.clear_default_graph()

    query = """
    PREFIX fdo: <http://example.org/fdo#>

    SELECT ?application
    WHERE {
        ?application a fdo:Application
    }
    """

    response = service.query(query)

    applications = response["results"]["bindings"]

    assert applications == []