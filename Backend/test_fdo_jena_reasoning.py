from pathlib import Path

import requests


FUSEKI_URL = "http://localhost:3030/fdo-reasoning/query"
FUSEKI_UPDATE_URL = "http://localhost:3030/fdo-reasoning/update"

PROJECT_ROOT = Path(__file__).resolve().parent
ONTOLOGY_PATH = PROJECT_ROOT / "ontology" / "FDO.owl"
TEST_DATA_PATH = PROJECT_ROOT / "ontology" / "fdo-test-data.ttl"

EXPECTED_DATA_URI = (
    "http://example.org/fdo#resource/expected-data/expected-001"
)

FDO_EXPECTED_DATA_URI = (
    "http://example.org/fdo#ExpectedData"
)

FDO_ENTITY_URI = (
    "http://example.org/fdo#FDOEntity"
)


def run_sparql(query: str) -> dict:
    response = requests.post(
        FUSEKI_URL,
        data={"query": query},
        headers={
            "Accept": "application/sparql-results+json",
        },
        timeout=30,
    )

    response.raise_for_status()
    return response.json()


def clear_dataset():
    response = requests.post(
        FUSEKI_UPDATE_URL,
        data={
            "update": "CLEAR DEFAULT",
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
        timeout=30,
    )

    response.raise_for_status()


def upload_file(path: Path, content_type: str):
    with path.open("rb") as file:
        response = requests.post(
            "http://localhost:3030/fdo-reasoning/data",
            data=file,
            headers={
                "Content-Type": content_type,
            },
            params={
                "default": "",
            },
            timeout=30,
        )

    response.raise_for_status()


def setup_reasoning_fixture():
    assert ONTOLOGY_PATH.exists(), (
        f"Missing ontology: {ONTOLOGY_PATH}"
    )

    assert TEST_DATA_PATH.exists(), (
        f"Missing test data: {TEST_DATA_PATH}"
    )

    clear_dataset()

    upload_file(
        ONTOLOGY_PATH,
        "application/rdf+xml",
    )

    upload_file(
        TEST_DATA_PATH,
        "text/turtle",
    )


def setup_module():
    setup_reasoning_fixture()


def test_fuseki_reasoning_endpoint_available():
    query = """
    SELECT * WHERE {
        ?s ?p ?o
    }
    LIMIT 1
    """

    result = run_sparql(query)

    assert "head" in result
    assert "results" in result
    assert "bindings" in result["results"]


def test_expected_data_explicit_type():
    query = f"""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

    SELECT ?type
    WHERE {{
        <{EXPECTED_DATA_URI}> rdf:type ?type .
    }}
    """

    result = run_sparql(query)

    types = {
        binding["type"]["value"]
        for binding in result["results"]["bindings"]
    }

    assert FDO_EXPECTED_DATA_URI in types


def test_jena_infers_fdo_entity():
    query = f"""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

    SELECT ?type
    WHERE {{
        <{EXPECTED_DATA_URI}> rdf:type ?type .
    }}
    """

    result = run_sparql(query)

    types = {
        binding["type"]["value"]
        for binding in result["results"]["bindings"]
    }

    assert FDO_ENTITY_URI in types


def test_reasoning_produces_inferred_triples():
    explicit_triple_count = 295 + 17

    query = """
    SELECT (COUNT(*) AS ?count)
    WHERE {
        ?s ?p ?o
    }
    """

    result = run_sparql(query)

    count = int(
        result["results"]["bindings"][0]["count"]["value"]
    )

    assert count > explicit_triple_count