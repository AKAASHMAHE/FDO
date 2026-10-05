from app.ontology.namespace import FDO
from app.ontology.rdf_instance_builder import (
    build_rdf_graph,
    add_overreach,
    add_personal_data,
    add_function,
    connect_overreach_data,
    connect_overreach_function,
)
from app.ontology.classes import (
    Overreach,
    PersonalData,
    Function,
)
from app.ontology.sparql_queries import (
    QUERY_ALL_OVERREACH,
)
from app.ontology.sparql_service import (
    execute_query,
    query_to_dicts,
)
from app.ontology.uri import (
    overreach_uri,
    personal_data_uri,
    function_uri,
)


def build_test_graph():
    graph = build_rdf_graph()

    add_personal_data(
        graph,
        PersonalData(
            id="location",
            name="Location",
        ),
    )

    add_function(
        graph,
        Function(
            id="navigation",
            name="Navigation",
        ),
    )

    add_overreach(
        graph,
        Overreach(
            id="overreach-1",
            name="Excessive Location Collection",
            status="FDO",
            reason="Location exceeds expected functional need",
            confidence=0.85,
        ),
    )

    connect_overreach_data(
        graph,
        "overreach-1",
        "location",
    )

    connect_overreach_function(
        graph,
        "overreach-1",
        "navigation",
    )

    return graph


def test_sparql_query_executes():
    graph = build_test_graph()

    results = execute_query(
        graph,
        QUERY_ALL_OVERREACH,
    )

    rows = list(results)

    assert len(rows) == 1


def test_sparql_finds_overreach():
    graph = build_test_graph()

    rows = query_to_dicts(
        graph,
        QUERY_ALL_OVERREACH,
    )

    assert len(rows) == 1

    assert rows[0]["overreach"] == str(
        overreach_uri("overreach-1")
    )


def test_sparql_returns_related_data():
    graph = build_test_graph()

    rows = query_to_dicts(
        graph,
        QUERY_ALL_OVERREACH,
    )

    assert rows[0]["data"] == str(
        personal_data_uri("location")
    )


def test_sparql_returns_related_function():
    graph = build_test_graph()

    rows = query_to_dicts(
        graph,
        QUERY_ALL_OVERREACH,
    )

    assert rows[0]["function"] == str(
        function_uri("navigation")
    )