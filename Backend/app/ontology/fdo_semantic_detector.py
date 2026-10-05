from rdflib import Graph

from .fdo_detection_queries import FDO_DETECTION_QUERY


STANDALONE_FDO_DETECTION_QUERY = """
PREFIX fdo: <http://example.org/fdo#>

SELECT
    ?expectedData
    ?declaredData
    ?expectedType
    ?declaredType
    ?expectedPurpose
    ?declaredPurpose
WHERE {
    ?expectedData a fdo:ExpectedData ;
                  fdo:dataType ?expectedType ;
                  fdo:purpose ?expectedPurpose .

    ?declaredData a fdo:DeclaredData ;
                  fdo:dataType ?declaredType ;
                  fdo:purpose ?declaredPurpose .

    FILTER (
        STR(?expectedType) != STR(?declaredType)
        ||
        STR(?expectedPurpose) != STR(?declaredPurpose)
    )
}
"""


def detect_fdo(graph: Graph) -> list[dict]:
    """
    Detect semantic FDO findings.

    Uses the full functional-context query first.
    Falls back to standalone expected-vs-declared
    comparison when no functional context exists.
    """

    results = graph.query(
        FDO_DETECTION_QUERY
    )

    findings = []

    for row in results:
        findings.append(
            {
                "application": str(row.application),
                "function": str(row.function),
                "expected_data": str(
                    row.expectedData
                ),
                "declared_data": str(
                    row.declaredData
                ),
                "expected_type": str(
                    row.expectedType
                ),
                "declared_type": str(
                    row.declaredType
                ),
                "expected_purpose": str(
                    row.expectedPurpose
                ),
                "declared_purpose": str(
                    row.declaredPurpose
                ),
            }
        )

    if findings:
        return findings

    standalone_results = graph.query(
        STANDALONE_FDO_DETECTION_QUERY
    )

    for row in standalone_results:
        findings.append(
            {
                "application": None,
                "function": None,
                "expected_data": str(
                    row.expectedData
                ),
                "declared_data": str(
                    row.declaredData
                ),
                "expected_type": str(
                    row.expectedType
                ),
                "declared_type": str(
                    row.declaredType
                ),
                "expected_purpose": str(
                    row.expectedPurpose
                ),
                "declared_purpose": str(
                    row.declaredPurpose
                ),
            }
        )

    return findings