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
from app.services.data_type_hierarchy import hierarchy_edges


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
    graph.add((FDO.DataType, RDF.type, OWL.Class))
    graph.add((FDO.DataType, RDFS.label, Literal("DataType")))
    graph.add(
        (
            FDO.DataType,
            RDFS.comment,
            Literal("Root class for canonical data-type taxonomy classes."),
        )
    )
    graph.add((FDO.AncillaryData, RDF.type, OWL.Class))
    graph.add((FDO.AncillaryData, RDFS.label, Literal("AncillaryData")))
    graph.add(
        (
            FDO.AncillaryData,
            RDFS.comment,
            Literal(
                "Declared data types and purposes covered by the "
                "cross-application ancillary baseline."
            ),
        )
    )

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

    def data_type_class(code: str):
        if code == "PersonalData":
            return FDO.PersonalData
        if code == "DataType":
            return FDO.DataType
        return FDO[f"DataType_{code.replace('.', '_')}"]

    for child, parent in hierarchy_edges():
        child_uri = data_type_class(child)
        parent_uri = data_type_class(parent)
        graph.add((child_uri, RDF.type, OWL.Class))
        graph.add((child_uri, RDFS.label, Literal(child)))
        graph.add(
            (
                child_uri,
                RDFS.comment,
                Literal(f"Data type taxonomy class for {child}."),
            )
        )
        graph.add((parent_uri, RDF.type, OWL.Class))
        if parent != "PersonalData":
            graph.add((parent_uri, RDFS.label, Literal(parent)))
            graph.add(
                (
                    parent_uri,
                    RDFS.comment,
                    Literal(f"Data type taxonomy class for {parent}."),
                )
            )
        graph.add((child_uri, RDFS.subClassOf, parent_uri))

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