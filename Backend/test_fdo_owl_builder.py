from rdflib import RDF, RDFS, OWL, XSD

from app.ontology.namespace import FDO
from app.ontology.owl_builder import build_fdo_ontology


def test_fdo_ontology_builds():
    graph = build_fdo_ontology()

    assert len(graph) > 0


def test_fdo_ontology_declares_ontology():
    graph = build_fdo_ontology()

    assert (
        FDO["Ontology"],
        RDF.type,
        OWL.Ontology,
    ) in graph


def test_core_fdo_classes_are_owl_classes():
    graph = build_fdo_ontology()

    expected_classes = [
        "Application",
        "Function",
        "PersonalData",
        "SensitiveData",
        "ProcessingActivity",
        "Purpose",
        "Recipient",
        "RetentionPolicy",
        "PrivacyPolicy",
        "PolicyClause",
        "ExpectedData",
        "DeclaredData",
        "Overreach",
        "Justification",
        "Risk",
    ]

    for class_name in expected_classes:
        assert (
            FDO[class_name],
            RDF.type,
            OWL.Class,
        ) in graph


def test_core_object_properties_are_owl_object_properties():
    graph = build_fdo_ontology()

    expected_properties = [
        "performsFunction",
        "requiresData",
        "collectsData",
        "expectedData",
        "usedForPurpose",
        "processedBy",
        "sharedWith",
        "hasRetentionPolicy",
        "hasJustification",
        "concernsData",
        "concernsFunction",
        "hasRisk",
    ]

    for property_name in expected_properties:
        assert (
            FDO[property_name],
            RDF.type,
            OWL.ObjectProperty,
        ) in graph


def test_core_data_properties_are_owl_datatype_properties():
    graph = build_fdo_ontology()

    expected_properties = [
        "id",
        "name",
        "description",
        "category",
        "sensitive",
        "dataType",
        "necessity",
        "purpose",
        "sharing",
        "retention",
        "reason",
        "confidence",
        "level",
        "score",
    ]

    for property_name in expected_properties:
        assert (
            FDO[property_name],
            RDF.type,
            OWL.DatatypeProperty,
        ) in graph


def test_performs_function_domain_and_range():
    graph = build_fdo_ontology()

    assert (
        FDO["performsFunction"],
        RDFS.domain,
        FDO["Application"],
    ) in graph

    assert (
        FDO["performsFunction"],
        RDFS.range,
        FDO["Function"],
    ) in graph


def test_requires_data_domain_and_range():
    graph = build_fdo_ontology()

    assert (
        FDO["requiresData"],
        RDFS.domain,
        FDO["Function"],
    ) in graph

    assert (
        FDO["requiresData"],
        RDFS.range,
        FDO["PersonalData"],
    ) in graph


def test_confidence_has_float_range():
    graph = build_fdo_ontology()

    assert (
        FDO["confidence"],
        RDFS.range,
        XSD.float,
    ) in graph


def test_sensitive_has_boolean_range():
    graph = build_fdo_ontology()

    assert (
        FDO["sensitive"],
        RDFS.range,
        XSD.boolean,
    ) in graph


def test_data_type_has_string_range():
    graph = build_fdo_ontology()

    assert (
        FDO["dataType"],
        RDFS.range,
        XSD.string,
    ) in graph