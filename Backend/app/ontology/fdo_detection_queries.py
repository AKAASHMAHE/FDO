"""
SPARQL queries for semantic FDO detection.
"""

FDO_DETECTION_QUERY = """
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
                  fdo:id ?dataId ;
                  fdo:dataType ?expectedType ;
                  fdo:purpose ?expectedPurpose .

    ?declaredData a fdo:DeclaredData ;
                  fdo:id ?dataId ;
                  fdo:dataType ?declaredType ;
                  fdo:purpose ?declaredPurpose .

    FILTER (
        STR(?expectedType) != STR(?declaredType)
        ||
        STR(?expectedPurpose) != STR(?declaredPurpose)
    )
}
"""


SENSITIVE_DATA_QUERY = """
PREFIX fdo: <http://example.org/fdo#>

SELECT
    ?data
    ?name
    ?category
WHERE {
    ?data a fdo:SensitiveData ;
         fdo:name ?name ;
         fdo:sensitive true .

    OPTIONAL {
        ?data fdo:sensitivityCategory ?category .
    }
}
"""