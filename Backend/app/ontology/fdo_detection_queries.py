"""
SPARQL queries for semantic FDO detection.
"""

FDO_DETECTION_QUERY = """
PREFIX fdo: <http://example.org/fdo#>

SELECT
    ?application
    ?function
    ?expectedData
    ?declaredData
    ?expectedType
    ?declaredType
    ?expectedPurpose
    ?declaredPurpose
WHERE {
    ?application a fdo:Application ;
                 fdo:performsFunction ?function ;
                 fdo:declaredData ?declaredData .

    ?function a fdo:Function ;
              fdo:expectedData ?expectedData .

    ?expectedData fdo:dataType ?expectedType ;
                  fdo:purpose ?expectedPurpose .

    ?declaredData fdo:dataType ?declaredType ;
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