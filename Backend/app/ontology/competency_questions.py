"""
FDO Ontology - Competency Questions

Defines the questions that the FDO ontology and knowledge graph
must be capable of answering.

These questions will later be implemented using SPARQL queries
and reasoning rules.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class CompetencyQuestion:
    """
    Represents a question that the FDO ontology must answer.
    """

    id: str
    question: str
    purpose: str
    expected_result: str


FDO_COMPETENCY_QUESTIONS = [

    CompetencyQuestion(
        id="CQ01",
        question="What functions does an application perform?",
        purpose="Identify the functional capabilities of an application.",
        expected_result="Application and associated Function entities.",
    ),

    CompetencyQuestion(
        id="CQ02",
        question="What personal data does a function reasonably require?",
        purpose="Identify functionally expected data.",
        expected_result="Function and required PersonalData entities.",
    ),

    CompetencyQuestion(
        id="CQ03",
        question="What personal data does an application collect?",
        purpose="Identify declared or observed data collection.",
        expected_result="Application and collected PersonalData entities.",
    ),

    CompetencyQuestion(
        id="CQ04",
        question="Which collected data is expected for a given function?",
        purpose="Compare functional data requirements with collected data.",
        expected_result="Expected and collected data relationships.",
    ),

    CompetencyQuestion(
        id="CQ05",
        question="Which collected data has no corresponding functional requirement?",
        purpose="Identify potential Functional Data Overreach.",
        expected_result="Data entities without matching functional requirements.",
    ),

    CompetencyQuestion(
        id="CQ06",
        question="For what purposes is personal data used?",
        purpose="Determine semantic purpose of data processing.",
        expected_result="PersonalData and Purpose relationships.",
    ),

    CompetencyQuestion(
        id="CQ07",
        question="Is the declared purpose compatible with the expected functional purpose?",
        purpose="Determine semantic purpose compatibility.",
        expected_result="Compatible, incompatible, or insufficient-evidence result.",
    ),

    CompetencyQuestion(
        id="CQ08",
        question="Which personal data is shared with external recipients?",
        purpose="Identify third-party data sharing.",
        expected_result="PersonalData and Recipient relationships.",
    ),

    CompetencyQuestion(
        id="CQ09",
        question="How long is personal data retained?",
        purpose="Identify retention information.",
        expected_result="PersonalData and RetentionPolicy relationships.",
    ),

    CompetencyQuestion(
        id="CQ10",
        question="Which policy clause provides evidence for a declared data practice?",
        purpose="Maintain traceability from semantic facts to policy evidence.",
        expected_result="DeclaredData and PolicyClause relationships.",
    ),

    CompetencyQuestion(
        id="CQ11",
        question="Which privacy policy contains a particular policy clause?",
        purpose="Trace extracted evidence to its source policy.",
        expected_result="PolicyClause and PrivacyPolicy relationship.",
    ),

    CompetencyQuestion(
        id="CQ12",
        question="Which data collection practices are associated with an FDO finding?",
        purpose="Identify the data involved in overreach.",
        expected_result="Overreach and PersonalData relationships.",
    ),

    CompetencyQuestion(
        id="CQ13",
        question="Which function is affected by a potential FDO finding?",
        purpose="Connect overreach findings to application functionality.",
        expected_result="Overreach and Function relationships.",
    ),

    CompetencyQuestion(
        id="CQ14",
        question="Why was a data practice classified as Functional Data Overreach?",
        purpose="Provide an explainable reason for the finding.",
        expected_result="Overreach and Justification information.",
    ),

    CompetencyQuestion(
        id="CQ15",
        question="What privacy risk is associated with an FDO finding?",
        purpose="Identify the risk associated with overreach.",
        expected_result="Overreach and Risk relationship.",
    ),

    CompetencyQuestion(
        id="CQ16",
        question="Which applications collect sensitive personal data?",
        purpose="Identify applications processing sensitive information.",
        expected_result="Application and SensitiveData relationships.",
    ),

    CompetencyQuestion(
        id="CQ17",
        question="Which applications collect data for purposes unrelated to their primary function?",
        purpose="Identify purpose-based Functional Data Overreach.",
        expected_result="Application, Function, PersonalData, and Purpose relationships.",
    ),

    CompetencyQuestion(
        id="CQ18",
        question="Which data practices have insufficient policy evidence?",
        purpose="Identify cases requiring ambiguous or cautious treatment.",
        expected_result="Data practices with missing or insufficient evidence.",
    ),

    CompetencyQuestion(
        id="CQ19",
        question="Which applications have potential Functional Data Overreach?",
        purpose="Produce application-level FDO findings.",
        expected_result="Applications associated with Overreach entities.",
    ),

    CompetencyQuestion(
        id="CQ20",
        question="What evidence supports an FDO decision for a specific application?",
        purpose="Provide complete explainability and traceability.",
        expected_result="Application, evidence, semantic relationships, and FDO finding.",
    ),
]
def get_competency_question(question_id: str) -> CompetencyQuestion:
    """
    Retrieve a competency question by ID.
    """

    for question in FDO_COMPETENCY_QUESTIONS:
        if question.id == question_id:
            return question

    raise KeyError(f"Unknown competency question: {question_id}")


def list_competency_question_ids() -> list[str]:
    """
    Return all competency question identifiers.
    """

    return [question.id for question in FDO_COMPETENCY_QUESTIONS]