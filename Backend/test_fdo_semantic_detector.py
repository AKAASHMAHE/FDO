from app.ontology.fdo_semantic_detector import detect_fdo
from app.ontology.rdf_instance_builder import build_rdf_graph


def test_semantic_detector_finds_type_mismatch():
    graph = build_rdf_graph(
        expected_data=[
            {
                "id": "location",
                "name": "Location",
                "data_type": "location",
                "necessity": "required",
                "purpose": "navigation",
            }
        ],
        declared_data=[
            {
                "id": "location",
                "name": "Location",
                "data_type": "precise_location",
                "purpose": "advertising",
            }
        ],
    )

    findings = detect_fdo(graph)

    assert len(findings) == 1
    assert findings[0]["expected_type"] != findings[0]["declared_type"]


def test_semantic_detector_returns_empty_for_matching_data():
    graph = build_rdf_graph(
        expected_data=[
            {
                "id": "phone-number",
                "name": "Phone Number",
                "data_type": "phone_number",
                "necessity": "required",
                "purpose": "communication",
            }
        ],
        declared_data=[
            {
                "id": "phone-number",
                "name": "Phone Number",
                "data_type": "phone_number",
                "purpose": "communication",
            }
        ],
    )

    findings = detect_fdo(graph)

    assert findings == []