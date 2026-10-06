from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.policy_document import PolicyDocument
from app.models.policy_evidence import PolicyEvidence


@dataclass
class PolicyAnalysisFinding:
    data_type: str | None
    data_label: str
    function: str
    purposes: list[str]
    evidence: list[str]
    confidence: float | None


@dataclass
class PolicyAnalysis:
    available: bool
    policy_source: str | None
    findings: list[PolicyAnalysisFinding]


def _label_from_data_type(data_type: str | None) -> str:
    if not data_type:
        return "Unclear Data"

    value = data_type.strip()

    if value.upper().startswith("DATA."):
        value = value[5:]

    words = [
        word
        for word in value.replace("-", ".").replace("_", ".").split(".")
        if word
    ]

    if len(words) > 1 and words[0].upper() == "MEDIA":
        words = words[1:]

    replacements = {
        "OTHER": "Other / Unclear Data",
        "CAMERA": "Camera",
        "MICROPHONE": "Microphone",
        "LOCATION": "Location",
        "PRECISE": "Precise",
        "APPROXIMATE": "Approximate",
        "CONTACTS": "Contacts",
        "DEVICE": "Device",
        "ACCOUNT": "Account",
        "FINANCIAL": "Financial",
        "HEALTH": "Health",
        "USAGE": "Usage",
    }

    return " ".join(
        replacements.get(word.upper(), word.capitalize())
        for word in words
    ) or "Unclear Data"


def _function_from_evidence(evidence: PolicyEvidence) -> str:
    if evidence.entity:
        return evidence.entity

    if evidence.purpose:
        return evidence.purpose

    return "Policy-declared processing"


def build_policy_analysis(
    session: Session,
    policy_id: str,
) -> PolicyAnalysis:
    policy = session.get(PolicyDocument, policy_id)

    if policy is None:
        return PolicyAnalysis(
            available=False,
            policy_source=None,
            findings=[],
        )

    evidence_rows = list(
        session.scalars(
            select(PolicyEvidence)
            .where(PolicyEvidence.policy_id == policy_id)
            .order_by(PolicyEvidence.evidence_id)
        )
    )

    grouped: dict[tuple[str | None, str], dict] = {}

    for evidence in evidence_rows:
        key = (
            evidence.data_type,
            _function_from_evidence(evidence),
        )

        if key not in grouped:
            grouped[key] = {
                "data_type": evidence.data_type,
                "data_label": _label_from_data_type(
                    evidence.data_type
                ),
                "function": _function_from_evidence(evidence),
                "purposes": [],
                "evidence": [],
                "confidence_values": [],
            }

        item = grouped[key]

        if evidence.purpose and evidence.purpose not in item["purposes"]:
            item["purposes"].append(evidence.purpose)

        if (
            evidence.evidence_text
            and evidence.evidence_text not in item["evidence"]
        ):
            item["evidence"].append(evidence.evidence_text)

        if evidence.confidence is not None:
            item["confidence_values"].append(evidence.confidence)

    findings = []

    for item in grouped.values():
        confidence_values = item.pop("confidence_values")
        confidence = (
            sum(confidence_values) / len(confidence_values)
            if confidence_values
            else None
        )

        findings.append(
            PolicyAnalysisFinding(
                confidence=confidence,
                **item,
            )
        )

    return PolicyAnalysis(
        available=bool(findings),
        policy_source=policy.source_identifier,
        findings=findings,
    )
