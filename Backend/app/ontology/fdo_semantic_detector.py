"""
Semantic FDO detector using RDF + SPARQL.
"""

from rdflib import Graph

from .fdo_detection_queries import FDO_DETECTION_QUERY


def detect_fdo(graph: Graph) -> list[dict]:
    """
    Detect potential FDO cases from the RDF graph.

    A mismatch is reported when expected and declared
    data type or purpose differ.
    """

    results = graph.query(FDO_DETECTION_QUERY)

    findings = []

    for row in results:
        findings.append(
            {
                "expected_data": str(row.expectedData),
                "declared_data": str(row.declaredData),
                "expected_type": str(row.expectedType),
                "declared_type": str(row.declaredType),
                "expected_purpose": str(row.expectedPurpose),
                "declared_purpose": str(row.declaredPurpose),
            }
        )

    return findings