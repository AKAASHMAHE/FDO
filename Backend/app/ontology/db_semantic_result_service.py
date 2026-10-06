from __future__ import annotations

from pathlib import Path
import json

from .db_semantic_repository import DBSemanticRepository
from .db_rdf_service import DBRDFService
from .semantic_fuseki_service import SemanticFusekiService
from .fuseki_semantic_detector import FusekiSemanticDetector
from .semantic_decision_adapter import decide_semantic_finding
from app.services.evidence_validation_service import (
    is_semantic_finding_usable,
)


def deduplicate_semantic_results(
    results: list[dict],
) -> list[dict]:
    deduplicated = []
    seen = set()

    for result in results:
        key = (
            result.get("application_id"),
            result.get("function"),
            result.get("expected_data"),
            result.get("declared_data"),
            result.get("expected_type"),
            result.get("declared_type"),
            result.get("expected_purpose"),
            result.get("declared_purpose"),
            result.get("fdo_status"),
        )

        if key in seen:
            continue

        seen.add(key)
        deduplicated.append(result)

    return deduplicated


def _purpose_items(value) -> list[str]:
    if value is None:
        return []

    if isinstance(value, list):
        return [
            str(item).strip()
            for item in value
            if str(item).strip()
        ]

    text = str(value).strip()

    if not text:
        return []

    try:
        parsed = json.loads(text)
    except (TypeError, ValueError):
        return [text]

    if isinstance(parsed, list):
        return [
            str(item).strip()
            for item in parsed
            if str(item).strip()
        ]

    return [text]


def group_semantic_result_purposes(
    results: list[dict],
) -> list[dict]:
    grouped = []
    index_by_key = {}

    for result in results:
        key = (
            result.get("application_id"),
            result.get("application"),
            result.get("function"),
            result.get("expected_data"),
            result.get("declared_data"),
            result.get("expected_type"),
            result.get("declared_type"),
            result.get("expected_purpose"),
            result.get("fdo_status"),
        )

        purposes = _purpose_items(
            result.get("declared_purposes")
            or result.get("declared_purpose")
        )

        if key not in index_by_key:
            grouped_result = dict(result)
            grouped_result["declared_purposes"] = []
            index_by_key[key] = len(grouped)
            grouped.append(grouped_result)

        grouped_result = grouped[index_by_key[key]]

        for purpose in purposes:
            if purpose not in grouped_result["declared_purposes"]:
                grouped_result["declared_purposes"].append(
                    purpose
                )

    for result in grouped:
        purposes = result.get("declared_purposes") or []
        result["declared_purpose"] = (
            json.dumps(purposes)
            if len(purposes) > 1
            else (purposes[0] if purposes else "")
        )

        if len(purposes) > 1:
            result["reason"] = (
                f"{result.get('reason', '')} "
                f"Grouped {len(purposes)} policy-declared purposes "
                "for the same function and data relationship."
            ).strip()

    return grouped


class DBSemanticResultService:
    """
    Runs semantic FDO analysis from real database records
    and returns unified structured results.
    """

    def __init__(
        self,
        repository: DBSemanticRepository,
        db_rdf_service: DBRDFService | None = None,
        fuseki_service: SemanticFusekiService | None = None,
    ):
        self.repository = repository

        self.db_rdf_service = (
            db_rdf_service
            or DBRDFService()
        )

        self.fuseki_service = (
            fuseki_service
            or SemanticFusekiService()
        )

    def analyze(
        self,
        application_id: str,
        policy_id: str,
        output_path: str | Path,
    ) -> list[dict]:

        application = self.repository.get_application(
            application_id
        )

        functions = self.repository.get_functions(
            application_id
        )

        expected_data = (
            self.repository.get_expected_mappings(
                application_id
            )
        )

        declared_data = (
            self.repository.get_policy_evidence(
                policy_id
            )
        )

        # ---------------------------------------------------------
        # Clear previous semantic analysis data
        # ---------------------------------------------------------

        self.fuseki_service.fuseki_service.clear_default_graph()

        # ---------------------------------------------------------
        # Build RDF graph from current DB records
        # ---------------------------------------------------------

        graph = self.db_rdf_service.build_graph(
            application=application,
            functions=functions,
            expected_data=expected_data,
            declared_data=declared_data,
        )

        # ---------------------------------------------------------
        # Publish current analysis graph to Fuseki
        # ---------------------------------------------------------

        self.fuseki_service.publish(
            graph,
            output_path,
        )

        # ---------------------------------------------------------
        # Detect semantic FDO findings
        # ---------------------------------------------------------

        detector = FusekiSemanticDetector(
            self.fuseki_service.fuseki_service
        )

        findings = detector.detect_fdo()

        results = []

        for finding in findings:

            if not finding["application"].endswith(
                f"/application/{application_id}"
            ):
                continue

            if not is_semantic_finding_usable(finding):
                continue

            decision = decide_semantic_finding(
                finding
            )

            results.append(
                {
                    "application_id": application_id,
                    "application": finding["application"],
                    "function": finding["function"],
                    "expected_data": finding["expected_data"],
                    "declared_data": finding["declared_data"],
                    "expected_type": finding["expected_type"],
                    "declared_type": finding["declared_type"],
                    "expected_purpose": finding["expected_purpose"],
                    "declared_purpose": finding["declared_purpose"],
                    "fdo_status": decision.fdo_status,
                    "confidence": decision.decision_confidence,
                    "reason": decision.decision_reason,
                }
            )

        return group_semantic_result_purposes(
            deduplicate_semantic_results(results)
        )
