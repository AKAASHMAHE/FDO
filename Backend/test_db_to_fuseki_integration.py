from app.ontology.db_rdf_service import DBRDFService
from app.ontology.semantic_fuseki_service import (
    SemanticFusekiService,
)


def test_db_rdf_to_fuseki_integration(tmp_path):

    rdf_service = DBRDFService()
    fuseki_service = SemanticFusekiService()

    graph = rdf_service.build_graph(
        application={
            "application_id": "integration-app-001",
            "application_name": "Integration Navigation App",
            "category": "Navigation",
            "description": "Integration test application",
        },
        functions=[
            {
                "function_record_id": "integration-func-001",
                "function_id": "navigation",
                "application_id": "integration-app-001",
                "function_name": "Navigation",
                "description": "Navigation function",
            }
        ],
        expected_data=[
            {
                "expected_id": "integration-expected-001",
                "application_id": "integration-app-001",
                "function_record_id": "integration-func-001",
                "data_type": "location",
                "necessity": "required",
                "expected_purpose": "navigation",
            }
        ],
        declared_data=[
            {
                "evidence_id": "integration-declared-001",
                "policy_id": "integration-policy-001",
                "data_type": "precise_location",
                "purpose": "advertising",
                "sharing": "third parties",
                "retention": "30 days",
            }
        ],
    )

    assert len(graph) > 0

    output_path = (
        tmp_path / "db-integration.ttl"
    )

    fuseki_service.publish(
        graph,
        output_path,
    )

    query = """
    PREFIX fdo: <http://example.org/fdo#>

    SELECT
        ?application
        ?function
        ?expectedData
        ?declaredData
    WHERE {
        ?application a fdo:Application ;
                     fdo:performsFunction ?function ;
                     fdo:declaredData ?declaredData .

        ?function a fdo:Function ;
                  fdo:expectedData ?expectedData .

        ?expectedData a fdo:ExpectedData .

        ?declaredData a fdo:DeclaredData .

        FILTER(
            STR(?application)
            =
            "http://example.org/fdo#resource/application/integration-app-001"
        )
    }
    """

    response = (
        fuseki_service.fuseki_service.query(query)
    )

    bindings = response["results"]["bindings"]

    assert len(bindings) >= 1

    row = bindings[0]

    assert row["application"]["value"].endswith(
        "/application/integration-app-001"
    )

    assert row["function"]["value"].endswith(
        "/function/integration-func-001"
    )

    assert row["expectedData"]["value"].endswith(
        "/expected-data/integration-expected-001"
    )

    assert row["declaredData"]["value"].endswith(
        "/declared-data/integration-declared-001"
    )