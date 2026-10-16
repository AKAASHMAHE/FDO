"""
SPARQL queries for semantic FDO detection.
"""

from app.services.data_type_hierarchy import canonical_data_type_code


def data_type_class_uri(data_type: str) -> str:
    canonical = canonical_data_type_code(data_type)
    return f"http://example.org/fdo#DataType_{canonical.replace('.', '_')}"


COVERED_QUERY = """
PREFIX fdo: <http://example.org/fdo#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT
    ?application ?applicationId ?function ?functionId ?functionName
    ?expectedData ?expectedId ?expectedType ?expectedClass
    ?expectedPurpose ?expectedNecessity
    ?declaredData ?declaredId ?declaredType ?declaredClass
    ?declaredPurpose ?extractionStatus ?confidence ?evidenceText ?entity
    ?typeRelation
WHERE {
    ?application a fdo:Application ;
                 fdo:id ?applicationId ;
                 fdo:performsFunction ?function ;
                 fdo:declaredData ?declaredData .
    ?function a fdo:Function ;
              fdo:id ?functionId ;
              fdo:expectedData ?expectedData .
    OPTIONAL { ?function fdo:name ?functionName }
    ?expectedData fdo:id ?expectedId ;
                  fdo:dataType ?expectedType ;
                  fdo:dataTypeClass ?expectedClass .
    OPTIONAL { ?expectedData fdo:purpose ?expectedPurpose }
    OPTIONAL { ?expectedData fdo:necessity ?expectedNecessity }
    ?declaredData fdo:id ?declaredId ;
                  fdo:dataType ?declaredType ;
                  fdo:dataTypeClass ?declaredClass .
    OPTIONAL { ?declaredData fdo:purpose ?declaredPurpose }
    OPTIONAL { ?declaredData fdo:extractionStatus ?extractionStatus }
    OPTIONAL { ?declaredData fdo:confidence ?confidence }
    OPTIONAL { ?declaredData fdo:text ?evidenceText }
    OPTIONAL { ?declaredData fdo:entity ?entity }
    FILTER (
        EXISTS { ?declaredClass rdfs:subClassOf* ?expectedClass }
        || EXISTS { ?expectedClass rdfs:subClassOf* ?declaredClass }
    )
    BIND(
        IF(
            ?expectedClass = ?declaredClass,
            "EXACT",
            IF(
                EXISTS { ?expectedClass rdfs:subClassOf+ ?declaredClass },
                "BROADER_EVIDENCE",
                "NARROWER_EVIDENCE"
            )
        )
        AS ?typeRelation
    )
}
"""

UNCOVERED_QUERY = """
PREFIX fdo: <http://example.org/fdo#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT
    ?application ?applicationId ?declaredData ?declaredId ?declaredType
    ?declaredClass ?declaredPurpose ?extractionStatus ?confidence
    ?evidenceText ?entity
WHERE {
    ?application a fdo:Application ;
                 fdo:id ?applicationId ;
                 fdo:declaredData ?declaredData .
    ?declaredData fdo:id ?declaredId ;
                  fdo:dataType ?declaredType ;
                  fdo:dataTypeClass ?declaredClass .
    OPTIONAL { ?declaredData fdo:purpose ?declaredPurpose }
    OPTIONAL { ?declaredData fdo:extractionStatus ?extractionStatus }
    OPTIONAL { ?declaredData fdo:confidence ?confidence }
    OPTIONAL { ?declaredData fdo:text ?evidenceText }
    OPTIONAL { ?declaredData fdo:entity ?entity }
    FILTER NOT EXISTS {
        ?application fdo:performsFunction ?function .
        ?function fdo:expectedData ?expectedData .
        ?expectedData fdo:dataTypeClass ?expectedClass .
        FILTER (
            EXISTS { ?declaredClass rdfs:subClassOf* ?expectedClass }
            || EXISTS { ?expectedClass rdfs:subClassOf* ?declaredClass }
        )
    }
}
"""

# Backward-compatible deprecated query for consumers of the former API.
FDO_DETECTION_QUERY = """
PREFIX fdo: <http://example.org/fdo#>

SELECT ?application ?function ?expectedData ?declaredData
       ?expectedType ?declaredType ?expectedPurpose ?declaredPurpose
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
        || STR(?expectedPurpose) != STR(?declaredPurpose)
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