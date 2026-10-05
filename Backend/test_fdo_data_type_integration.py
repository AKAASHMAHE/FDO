from rdflib import RDF

from app.ontology.namespace import FDO
from app.ontology.classes import ExpectedData, DeclaredData
from app.ontology.rdf_instance_builder import (
    build_rdf_graph,
    connect_expected_data_personal_data,
    connect_declared_data_personal_data,
)
from app.ontology.uri import (
    expected_data_uri,
    declared_data_uri,
    personal_data_uri,
)


def test_location_maps_to_personal_data():
    graph = build_rdf_graph(
        expected_data=[
            ExpectedData(
                id="exp-1",
                name="Location",
                data_type="location",
            )
        ]
    )

    data_uri = personal_data_uri("location")

    assert data_uri is not None


def test_expected_data_can_connect_to_personal_data():
    graph = build_rdf_graph(
        expected_data=[
            ExpectedData(
                id="exp-1",
                name="Location",
                data_type="location",
            )
        ]
    )

    connect_expected_data_personal_data(
        graph,
        "exp-1",
        "location",
    )

    assert (
        expected_data_uri("exp-1"),
        FDO.expectedDataType,
        personal_data_uri("location"),
    ) in graph


def test_declared_data_can_connect_to_personal_data():
    graph = build_rdf_graph(
        declared_data=[
            DeclaredData(
                id="decl-1",
                name="Location",
                data_type="location",
            )
        ]
    )

    connect_declared_data_personal_data(
        graph,
        "decl-1",
        "location",
    )

    assert (
        declared_data_uri("decl-1"),
        FDO.declaredDataType,
        personal_data_uri("location"),
    ) in graph


def test_same_data_type_has_stable_uri():
    first = personal_data_uri("location")
    second = personal_data_uri("location")

    assert first == second


def test_data_type_names_are_case_insensitive():
    graph = build_rdf_graph(
        expected_data=[
            ExpectedData(
                id="exp-1",
                name="Location",
                data_type="LOCATION",
            )
        ]
    )

    connect_expected_data_personal_data(
        graph,
        "exp-1",
        "LOCATION",
    )

    assert (
        expected_data_uri("exp-1"),
        FDO.expectedDataType,
        personal_data_uri("location"),
    ) in graph


def test_multiple_data_types_remain_distinct():
    location = personal_data_uri("location")
    email = personal_data_uri("email")
    phone = personal_data_uri("phone")

    assert location != email
    assert email != phone
    assert location != phone