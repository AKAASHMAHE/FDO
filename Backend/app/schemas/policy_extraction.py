from pydantic import BaseModel


class PolicyExtractionRequest(BaseModel):
    policy_text: str
    application_name: str


class PolicyEvidenceResponse(BaseModel):
    evidence_id: str
    data_type: str | None
    purpose: str | None
    entity: str | None
    sharing: str | None
    retention: str | None
    evidence_text: str
    source_section: str | None
    extraction_status: str
    confidence: float | None


class PolicyExtractionResponse(BaseModel):
    extraction_status: str
    evidence: list[PolicyEvidenceResponse]