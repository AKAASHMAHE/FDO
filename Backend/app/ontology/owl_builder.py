"""
FDO OWL Ontology Builder.

Builds the formal Functional Data Ontology as an RDFLib graph.

The builder converts the Python semantic specification into
OWL/RDF concepts:

    - owl:Class
    - owl:ObjectProperty
    - owl:DatatypeProperty
    - rdfs:domain
    - rdfs:range
    - rdfs:label
    - rdfs:comment

This module creates the ontology schema only.

Instance generation will be implemented separately.
"""

from rdflib import Graph, Literal, RDF, RDFS, OWL, XSD

from .namespace import FDO, FDO_NAMESPACE_URI
from .specification import get_fdo_specification


def build_fdo_ontology() -> Graph:
    """
    Build the complete FDO OWL ontology schema.

    Returns:
        RDFLib Graph containing the FDO ontology.
    """

    graph = Graph()

    # ------------------------------------------------------------------
    # Namespace
    # ------------------------------------------------------------------

    graph.bind("fdo", FDO)
    graph.bind("owl", OWL)
    graph.bind("rdfs", RDFS)

    # ------------------------------------------------------------------
    # Ontology declaration
    # ------------------------------------------------------------------

    ontology_uri = FDO["Ontology"]

    graph.add(
        (
            ontology_uri,
            RDF.type,
            OWL.Ontology,
        )
    )

    graph.add(
        (
            ontology_uri,
            RDFS.label,
            Literal("Functional Data Ontology"),
        )
    )

    graph.add(
        (
            ontology_uri,
            RDFS.comment,
            Literal(
                "Ontology for semantic analysis of application "
                "functionality, personal data processing, privacy "
                "policy evidence, and Functional Data Overreach."
            ),
        )
    )

    # ------------------------------------------------------------------
    # Classes
    # ------------------------------------------------------------------

    specification = get_fdo_specification()

    for class_name, class_type in specification.classes.items():

        class_uri = FDO[class_name]

        graph.add(
            (
                class_uri,
                RDF.type,
                OWL.Class,
            )
        )

        graph.add(
            (
                class_uri,
                RDFS.label,
                Literal(class_name),
            )
        )

        graph.add(
            (
                class_uri,
                RDFS.comment,
                Literal(
                    f"FDO semantic class representing {class_name}."
                ),
            )
        )

    # ------------------------------------------------------------------
    # Object Properties
    # ------------------------------------------------------------------

    for property_name, property_definition in (
        specification.object_properties.items()
    ):

        property_uri = FDO[property_name]

        graph.add(
            (
                property_uri,
                RDF.type,
                OWL.ObjectProperty,
            )
        )

        graph.add(
            (
                property_uri,
                RDFS.label,
                Literal(property_name),
            )
        )

        graph.add(
            (
                property_uri,
                RDFS.domain,
                FDO[property_definition.domain.__name__],
            )
        )

        graph.add(
            (
                property_uri,
                RDFS.range,
                FDO[property_definition.range.__name__],
            )
        )

        graph.add(
            (
                property_uri,
                RDFS.comment,
                Literal(property_definition.description),
            )
        )

    # ------------------------------------------------------------------
    # Data Properties
    # ------------------------------------------------------------------

    datatype_mapping = {
        "string": XSD.string,
        "boolean": XSD.boolean,
        "float": XSD.float,
        "integer": XSD.integer,
    }

    for property_name, property_definition in (
        specification.data_properties.items()
    ):

        property_uri = FDO[property_name]

        graph.add(
            (
                property_uri,
                RDF.type,
                OWL.DatatypeProperty,
            )
        )

        graph.add(
            (
                property_uri,
                RDFS.label,
                Literal(property_name),
            )
        )

        graph.add(
            (
                property_uri,
                RDFS.domain,
                FDO[property_definition.domain.__name__],
            )
        )

        datatype_uri = datatype_mapping.get(
            property_definition.datatype,
            XSD.string,
        )

        graph.add(
            (
                property_uri,
                RDFS.range,
                datatype_uri,
            )
        )

        graph.add(
            (
                property_uri,
                RDFS.comment,
                Literal(property_definition.description),
            )
        )

    return graph


def serialize_fdo_ontology(
    output_path: str,
    format: str = "xml",
) -> str:
    """
    Build and serialize the FDO ontology.

    Args:
        output_path: Destination file path.
        format: RDFLib serialization format.

    Returns:
        Output path.
    """

    graph = build_fdo_ontology()

    graph.serialize(
        destination=output_path,
        format=format,
    )

    return output_path