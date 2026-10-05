import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.ontology.classes import (
    Application,
    Function,
    ExpectedData,
    DeclaredData,
)
from app.ontology.rdf_instance_builder import (
    build_rdf_graph,
    connect_application_function,
    connect_function_expected_data,
    connect_application_declared_data,
)
from app.ontology.rdf_export_service import export_rdf_graph


def main():
    graph = build_rdf_graph(
        applications=[
            Application(
                id="app-001",
                name="Navigation App",
            )
        ],
        functions=[
            Function(
                id="func-001",
                name="Navigation",
            )
        ],
        expected_data=[
            ExpectedData(
                id="expected-001",
                name="Location",
                data_type="location",
                necessity="required",
                purpose="navigation",
            )
        ],
        declared_data=[
            DeclaredData(
                id="declared-001",
                name="Precise Location",
                data_type="precise_location",
                purpose="advertising",
            )
        ],
    )

    # Connect the application to its function.
    connect_application_function(
        graph,
        application_id="app-001",
        function_id="func-001",
    )

    # Connect the function to the data it reasonably expects.
    connect_function_expected_data(
        graph,
        function_id="func-001",
        expected_id="expected-001",
    )

    # Connect the application to the data it declares/collects.
    connect_application_declared_data(
        graph,
        application_id="app-001",
        declared_id="declared-001",
    )

    output = Path("ontology/fdo-test-data.ttl")

    export_rdf_graph(
        graph,
        output,
        format="turtle",
    )

    print(f"Exported RDF: {output}")
    print(f"Triple count: {len(graph)}")


if __name__ == "__main__":
    main()