"""
Reusable SPARQL queries for the FDO semantic layer.
"""

FDO_PREFIX = """
PREFIX fdo: <http://example.org/fdo#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
"""

QUERY_ALL_OVERREACH = FDO_PREFIX + """
SELECT ?overreach ?data ?function
WHERE {
    ?overreach rdf:type fdo:Overreach .
    OPTIONAL {
        ?overreach fdo:concernsData ?data .
    }
    OPTIONAL {
        ?overreach fdo:concernsFunction ?function .
    }
}
"""

QUERY_OVERREACH_DETAILS = FDO_PREFIX + """
SELECT ?overreach ?data ?function ?justification ?risk
WHERE {
    ?overreach rdf:type fdo:Overreach .

    OPTIONAL {
        ?overreach fdo:concernsData ?data .
    }

    OPTIONAL {
        ?overreach fdo:concernsFunction ?function .
    }

    OPTIONAL {
        ?overreach fdo:hasJustification ?justification .
    }

    OPTIONAL {
        ?overreach fdo:hasRisk ?risk .
    }
}
"""

QUERY_SENSITIVE_DATA = FDO_PREFIX + """
SELECT ?data ?category
WHERE {
    ?data rdf:type fdo:SensitiveData .
    OPTIONAL {
        ?data fdo:sensitivityCategory ?category .
    }
}
"""

QUERY_DATA_BY_PURPOSE = FDO_PREFIX + """
SELECT ?data ?purpose
WHERE {
    ?data rdf:type fdo:PersonalData .
    ?data fdo:usedForPurpose ?purpose .
}
"""