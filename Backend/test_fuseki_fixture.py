from pathlib import Path

import requests


FUSEKI_BASE_URL = "http://localhost:3030/fdo-reasoning"

PROJECT_ROOT = Path(__file__).resolve().parent

ONTOLOGY_PATH = PROJECT_ROOT / "ontology" / "FDO.owl"


TEST_DATA = """
<http://example.org/fdo#resource/application/app-001>
    a <http://example.org/fdo#Application> ;
    <http://example.org/fdo#id> "app-001" ;
    <http://example.org/fdo#name> "Test Navigation App" ;
    <http://example.org/fdo#performsFunction>
        <http://example.org/fdo#resource/function/func-001> ;
    <http://example.org/fdo#declaredData>
        <http://example.org/fdo#resource/declared-data/evidence-001> .

<http://example.org/fdo#resource/function/func-001>
    a <http://example.org/fdo#Function> ;
    <http://example.org/fdo#id> "func-001" ;
    <http://example.org/fdo#name> "Location Navigation" ;
    <http://example.org/fdo#requiresData>
        <http://example.org/fdo#resource/expected-data/expected-001> ;
    <http://example.org/fdo#expectedData>
        <http://example.org/fdo#resource/expected-data/expected-001> .

<http://example.org/fdo#resource/expected-data/expected-001>
    a <http://example.org/fdo#ExpectedData> ;
    <http://example.org/fdo#id> "expected-001" ;
    <http://example.org/fdo#name> "Location" ;
    <http://example.org/fdo#dataType> "location" ;
    <http://example.org/fdo#necessity> "required" ;
    <http://example.org/fdo#purpose> "navigation" .

<http://example.org/fdo#resource/declared-data/evidence-001>
    a <http://example.org/fdo#DeclaredData> ;
    <http://example.org/fdo#id> "evidence-001" ;
    <http://example.org/fdo#name> "Precise Location" ;
    <http://example.org/fdo#dataType> "precise_location" ;
    <http://example.org/fdo#purpose> "advertising" .
"""


def setup_fuseki_semantic_fixture():
    # 1. Clear the reasoning dataset.
    clear_response = requests.post(
        f"{FUSEKI_BASE_URL}/update",
        data={
            "update": "CLEAR DEFAULT"
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        },
        timeout=30,
    )

    clear_response.raise_for_status()

    # 2. Upload the canonical FDO ontology.
    with ONTOLOGY_PATH.open("rb") as file:
        ontology_response = requests.post(
            f"{FUSEKI_BASE_URL}/data",
            params={"default": ""},
            data=file,
            headers={
                "Content-Type": "application/rdf+xml"
            },
            timeout=30,
        )

    ontology_response.raise_for_status()

    # 3. Insert deterministic semantic test data.
    fixture_update = f"""
INSERT DATA {{
{TEST_DATA}
}}
"""

    update_response = requests.post(
        f"{FUSEKI_BASE_URL}/update",
        data={
            "update": fixture_update
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        },
        timeout=30,
    )

    update_response.raise_for_status()