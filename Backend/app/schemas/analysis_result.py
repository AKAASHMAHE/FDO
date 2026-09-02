from pydantic import BaseModel


class AnalysisResultResponse(BaseModel):
    expected_id: str
    evidence_id: str | None

    data_match: str
    purpose_compatibility: str
    functional_relationship: str
    functional_justification: str
    evidence_status: str

    fdo_status: str
    decision_reason: str
    decision_confidence: float | None

    expected_necessity: str | None = None
    expected_purpose: str | None = None
    declared_data_type: str | None = None
    declared_purpose: str | None = None
    explanation: str | None = None
    evidence_available: bool | None = None