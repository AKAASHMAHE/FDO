from rdflib import RDF

from app.ontology.namespace import FDO
from app.ontology.classes import PersonalData, SensitiveData
from app.ontology.rdf_instance_builder import (
    build_rdf_graph,
    add_sensitive_data,
)
from app.ontology.uri import personal_data_uri


def test_sensitive_data_is_created_as_sensitive_data_class():
    graph = build_rdf_graph()

    add_sensitive_data(
        graph,
        SensitiveData(
            id="health",
            name="Health Information",
            sensitivity_category="health",
        ),
    )

    assert (
        personal_data_uri("health"),
        RDF.type,
        FDO.SensitiveData,
    ) in graph


def test_sensitive_data_is_also_personal_data():
    graph = build_rdf_graph()

    add_sensitive_data(
        graph,
        SensitiveData(
            id="financial",
            name="Financial Information",
            sensitivity_category="financial",
        ),
    )

    assert (
        personal_data_uri("financial"),
        RDF.type,
        FDO.PersonalData,
    ) in graph


def test_sensitive_data_has_sensitivity_category():
    graph = build_rdf_graph()

    add_sensitive_data(
        graph,
        SensitiveData(
            id="biometric",
            name="Biometric Information",
            sensitivity_category="biometric",
        ),
    )

    assert str(
    graph.value(
        personal_data_uri("biometric"),
        FDO.sensitivityCategory,
    )
) == "biometric"


def test_sensitive_data_is_marked_sensitive():
    graph = build_rdf_graph()

    add_sensitive_data(
        graph,
        SensitiveData(
            id="health",
            name="Health Information",
            sensitivity_category="health",
        ),
    )

    assert graph.value(
    personal_data_uri("health"),
    FDO.sensitive,
).toPython() is True


def test_sensitive_data_categories_remain_distinct():
    graph = build_rdf_graph()

    add_sensitive_data(
        graph,
        SensitiveData(
            id="health",
            name="Health Information",
            sensitivity_category="health",
        ),
    )

    add_sensitive_data(
        graph,
        SensitiveData(
            id="financial",
            name="Financial Information",
            sensitivity_category="financial",
        ),
    )

    assert str(
    graph.value(
        personal_data_uri("health"),
        FDO.sensitivityCategory,
    )
) == "health"

    assert str(
    graph.value(
        personal_data_uri("financial"),
        FDO.sensitivityCategory,
    )
) == "financial"

    assert personal_data_uri("health") != personal_data_uri("financial")


def test_normal_personal_data_is_not_sensitive_data():
    graph = build_rdf_graph(
        personal_data=[
            PersonalData(
                id="email",
                name="Email",
                sensitive=False,
            )
        ]
    )

    assert (
        personal_data_uri("email"),
        RDF.type,
        FDO.PersonalData,
    ) in graph

    assert (
        personal_data_uri("email"),
        RDF.type,
        FDO.SensitiveData,
    ) not in graph