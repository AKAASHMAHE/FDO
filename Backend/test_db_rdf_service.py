from app.ontology.db_rdf_service import DBRDFService


def test_db_rdf_service_builds_application_graph():

    service = DBRDFService()

    graph = service.build_graph(
        application={
            "application_id": "app-test",
            "application_name": "Test App",
            "category": "Navigation",
            "description": "Test navigation application",
        },
        functions=[
            {
                "function_record_id": "func-test",
                "function_id": "navigation",
                "application_id": "app-test",
                "function_name": "Navigation",
                "description": "Navigation feature",
            }
        ],
        expected_data=[
            {
                "expected_id": "expected-test",
                "application_id": "app-test",
                "function_record_id": "func-test",
                "data_type": "location",
                "necessity": "required",
                "expected_purpose": "navigation",
            }
        ],
        declared_data=[
            {
                "evidence_id": "declared-test",
                "policy_id": "policy-test",
                "data_type": "precise_location",
                "purpose": "advertising",
                "sharing": "third parties",
                "retention": "30 days",
            }
        ],
    )

    assert len(graph) > 0

    assert any(
        str(subject).endswith(
            "/application/app-test"
        )
        for subject in graph.subjects()
    )

    assert any(
        str(subject).endswith(
            "/function/func-test"
        )
        for subject in graph.subjects()
    )

    assert any(
        str(subject).endswith(
            "/expected-data/expected-test"
        )
        for subject in graph.subjects()
    )

    assert any(
        str(subject).endswith(
            "/declared-data/declared-test"
        )
        for subject in graph.subjects()
    )