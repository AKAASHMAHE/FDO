import json
import re

from pydantic import BaseModel, ConfigDict, Field, computed_field


def _format_identifier_label(value: str | None) -> str:
    if not value:
        return "Unknown"

    label = str(value).strip()

    resource_match = re.search(
        r"/resource/(?:function|expected-data|declared-data)/(.+)$",
        label,
    )
    if resource_match:
        label = resource_match.group(1)

    if ":" in label:
        label = label.split(":")[-1]

    label = re.sub(r"^(EXP|AI)[-_.]*", "", label, flags=re.I)
    label = re.sub(r"^(DATA|FUNC)[._-]", "", label, flags=re.I)

    words = [word for word in re.split(r"[._-]+", label) if word]

    if len(words) > 1 and words[0].upper() == "MEDIA":
        words = words[1:]

    replacements = {
        "COM": "Communication",
        "COMM": "Communication",
        "VIDEO": "Video",
        "CALL": "Call",
        "MEDIA": "Media",
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
        "OTHER": "Other / Unclear Data",
    }

    return " ".join(
        replacements.get(word.upper(), word.capitalize())
        for word in words
    ) or "Unknown"

class AnalysisCreateRequest(BaseModel):
    application_id: str
class ComparisonResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    comparison_id: str
    analysis_id: str
    expected_id: str
    evidence_id: str | None

    data_match: str
    data_match_relation: str = "NONE"
    purpose_compatibility: str
    functional_relationship: str
    functional_justification: str
    evidence_status: str


class FDOResultResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    result_id: str
    comparison_id: str
    fdo_status: str
    decision_reason: str
    decision_confidence: float | None
    created_at: str
class SemanticFDOResultResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    semantic_result_id: str

    application_id: str
    application: str
    function: str

    expected_data: str
    declared_data: str

    expected_type: str
    declared_type: str
    data_match_relation: str = "NONE"

    expected_purpose: str
    declared_purpose: str

    fdo_status: str
    confidence: float | None
    reason: str

    @computed_field
    @property
    def function_label(self) -> str:
        return _format_identifier_label(self.function)

    @computed_field
    @property
    def expected_data_label(self) -> str:
        return _format_identifier_label(
            self.expected_type or self.expected_data
        )

    @computed_field
    @property
    def declared_data_label(self) -> str:
        return _format_identifier_label(
            self.declared_type or self.declared_data
        )

    @computed_field
    @property
    def declared_purposes(self) -> list[str]:
        value = self.declared_purpose

        if not value:
            return []

        try:
            parsed = json.loads(value)
        except (TypeError, ValueError):
            return [value]

        if isinstance(parsed, list):
            return [
                str(item)
                for item in parsed
                if str(item).strip()
            ]

        return [value]


class PolicyAnalysisFindingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    data_type: str | None = None
    data_label: str
    function: str
    purposes: list[str] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)
    confidence: float | None = None


class PolicyAnalysisResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    available: bool = False
    policy_source: str | None = None
    findings: list[PolicyAnalysisFindingResponse] = Field(
        default_factory=list
    )


class FunctionalBaselineItemResponse(BaseModel):
    expected_id: str
    function_id: str | None = None
    function_name: str
    expected_data_type: str
    necessity: str
    expected_purpose: str
    baseline_source: str
    baseline_confidence: float | None = None
    baseline_justification: str | None = None
    
class AnalysisHistoryResponse(BaseModel):
    analysis_id: str
    application_id: str
    application_name: str
    category: str
    policy_id: str
    analysis_status: str
    total_mappings: int
    fdo_count: int
    not_fdo_count: int
    ambiguous_count: int
    created_at: str
    
class AnalysisReportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    analysis_id: str
    application_id: str
    policy_id: str
    analysis_status: str

    total_mappings: int
    fdo_count: int
    not_fdo_count: int
    ambiguous_count: int

    comparisons: list[ComparisonResponse]
    fdo_results: list[FDOResultResponse]
    semantic_results: list[SemanticFDOResultResponse] = Field(
        default_factory=list
    )
    policy_analysis: PolicyAnalysisResponse | None = None
    has_expected_baseline: bool = False
    baseline_source: str | None = None
    baseline_confidence: float | None = None
    baseline_status: str = "UNAVAILABLE"
    functional_baseline: list[
        FunctionalBaselineItemResponse
    ] = Field(default_factory=list)
class ApplicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    application_id: str
    application_name: str
    category: str
    description: str | None
class ApplicationReadinessResponse(BaseModel):
    application_id: str
    application_name: str
    category: str

    policy_count: int
    evidence_count: int

    ready_for_analysis: bool
class FunctionResponse(BaseModel):
    function_id: str
    function_name: str
    feature: str | None


class ApplicationDetailResponse(BaseModel):
    application_id: str
    application_name: str
    category: str
    description: str | None
    functions: list[FunctionResponse]
class ExpectedMappingResponse(BaseModel):
    expected_id: str
    function_id: str
    data_type: str
    necessity: str
    expected_purpose: str


class ExpectedMappingsResponse(BaseModel):
    application_id: str
    expected_mappings: list[ExpectedMappingResponse]
class AnalyzeRequest(BaseModel):
    application_name: str
    category: str = "Other"
    description: str | None = None
    policy_text: str | None = None
    policy_source: str | None = None
