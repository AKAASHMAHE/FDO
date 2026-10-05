from app.ontology.fuseki_service import FusekiService


def test_fuseki_query():
    service = FusekiService()

    result = service.query(
        """
        SELECT * WHERE {
            ?s ?p ?o
        }
        LIMIT 1
        """
    )

    assert "head" in result
    assert "results" in result