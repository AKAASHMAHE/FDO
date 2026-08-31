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