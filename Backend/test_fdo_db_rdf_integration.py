from rdflib import RDF

from app.ontology.namespace import FDO
from app.ontology.rdf_instance_builder import build_rdf_graph
from app.ontology.uri import (
    application_uri,
    function_uri,
    expected_data_uri,
    declared_data_uri,
)


def test_db_shaped_application_can_be_converted_to_rdf():
    graph = build_rdf_graph(
        applications=[
            {
                "id": "whatsapp",
                "name": "WhatsApp",
            }
        ]
    )

    assert (
        application_uri("whatsapp"),
        RDF.type,
        FDO.Application,
    ) in graph


def test_db_shaped_function_can_be_converted_to_rdf():
    graph = build_rdf_graph(
        functions=[
            {
                "id": "messaging",
                "name": "Messaging",
            }
        ]
    )

    assert (
        function_uri("messaging"),
        RDF.type,
        FDO.Function,
    ) in graph


def test_db_shaped_expected_data_can_be_converted_to_rdf():
    graph = build_rdf_graph(
        expected_data=[
            {
                "id": "phone-number",
                "name": "Phone Number",
                "data_type": "phone_number",
                "necessity": "required",
                "purpose": "communication",
            }
        ]
    )

    assert (
        expected_data_uri("phone-number"),
        RDF.type,
        FDO.ExpectedData,
    ) in graph


def test_db_shaped_declared_data_can_be_converted_to_rdf():
    graph = build_rdf_graph(
        declared_data=[
            {
                "id": "phone-number",
                "name": "Phone Number",
                "data_type": "phone_number",
                "purpose": "communication",
            }
        ]
    )

    assert (
        declared_data_uri("phone-number"),
        RDF.type,
        FDO.DeclaredData,
    ) in graph


def test_db_shaped_records_can_exist_together():
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
        expected_data=[
            {
                "id": "phone-number",
                "name": "Phone Number",
                "data_type": "phone_number",
                "necessity": "required",
                "purpose": "communication",
            }
        ],
        declared_data=[
            {
                "id": "phone-number",
                "name": "Phone Number",
                "data_type": "phone_number",
                "purpose": "communication",
            }
        ],
    )

    assert (
        application_uri("whatsapp"),
        RDF.type,
        FDO.Application,
    ) in graph

    assert (
        function_uri("messaging"),
        RDF.type,
        FDO.Function,
    ) in graph

    assert (
        expected_data_uri("phone-number"),
        RDF.type,
        FDO.ExpectedData,
    ) in graph

    assert (
        declared_data_uri("phone-number"),
        RDF.type,
        FDO.DeclaredData,
    ) in graph