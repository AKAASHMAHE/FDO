from __future__ import annotations

from rdflib import Graph

from .db_rdf_mapper import (
    application_from_record,
    function_from_record,
    expected_data_from_record,
    declared_data_from_record,
)

from .rdf_instance_builder import (
    add_data_type_taxonomy,
    add_application,
    add_function,
    add_expected_data,
    add_declared_data,
    connect_application_function,
    connect_function_expected_data,
    connect_application_declared_data,
)


class DBRDFService:
    """
    Converts database-shaped application analysis records
    into an FDO RDF graph.
    """

    def build_graph(
        self,
        application,
        functions,
        expected_data,
        declared_data,
    ) -> Graph:

        graph = Graph()

        graph.bind(
            "fdo",
            "http://example.org/fdo#",
        )
        add_data_type_taxonomy(graph)

        application_obj = application_from_record(
            application
        )

        add_application(
            graph,
            application_obj,
        )

        for record in functions:

            function_obj = function_from_record(
                record
            )

            add_function(
                graph,
                function_obj,
            )

            connect_application_function(
                graph,
                application_obj.id,
                function_obj.id,
            )

        for record in expected_data:

            expected_obj = expected_data_from_record(
                record
            )

            add_expected_data(
                graph,
                expected_obj,
            )

            function_record_id = getattr(
                record,
                "function_record_id",
                None,
            )

            if isinstance(record, dict):
                function_record_id = record.get(
                    "function_record_id"
                )

            if function_record_id:

                connect_function_expected_data(
                    graph,
                    function_record_id,
                    expected_obj.id,
                )

        for record in declared_data:

            declared_obj = declared_data_from_record(
                record
            )

            add_declared_data(
                graph,
                declared_obj,
            )

            connect_application_declared_data(
                graph,
                application_obj.id,
                declared_obj.id,
            )

        return graph