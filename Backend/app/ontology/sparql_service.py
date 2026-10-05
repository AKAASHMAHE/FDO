"""
SPARQL execution service for the FDO RDF graph.
"""

from rdflib import Graph


def execute_query(graph: Graph, query: str):
    """
    Execute a SPARQL query against an RDF graph.
    """
    return graph.query(query)


def query_to_dicts(graph: Graph, query: str) -> list[dict]:
    """
    Execute a SPARQL query and convert rows into dictionaries.
    """
    results = graph.query(query)

    rows = []

    for row in results:
        row_dict = {}

        for variable in results.vars:
            value = row[variable]
            row_dict[str(variable)] = (
                str(value) if value is not None else None
            )

        rows.append(row_dict)

    return rows