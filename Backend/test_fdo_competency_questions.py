from app.ontology import (
    CompetencyQuestion,
    FDO_COMPETENCY_QUESTIONS,
    get_competency_question,
    list_competency_question_ids,
)


def test_competency_question_structure():
    question = FDO_COMPETENCY_QUESTIONS[0]

    assert isinstance(question, CompetencyQuestion)
    assert question.id
    assert question.question
    assert question.purpose
    assert question.expected_result


def test_twenty_competency_questions_exist():
    assert len(FDO_COMPETENCY_QUESTIONS) == 20


def test_competency_question_ids_are_unique():
    ids = [
        question.id
        for question in FDO_COMPETENCY_QUESTIONS
    ]

    assert len(ids) == len(set(ids))


def test_competency_question_ids_are_sequential():
    ids = [
        question.id
        for question in FDO_COMPETENCY_QUESTIONS
    ]

    expected = [
        f"CQ{i:02d}"
        for i in range(1, 21)
    ]

    assert ids == expected


def test_get_competency_question():
    question = get_competency_question("CQ05")

    assert question.id == "CQ05"
    assert "functional requirement" in question.question.lower()


def test_unknown_competency_question():
    try:
        get_competency_question("CQ99")
        assert False
    except KeyError:
        assert True


def test_list_competency_question_ids():
    ids = list_competency_question_ids()

    assert len(ids) == 20
    assert ids[0] == "CQ01"
    assert ids[-1] == "CQ20"


def test_fdo_detection_question_exists():
    questions = {
        question.id: question
        for question in FDO_COMPETENCY_QUESTIONS
    }

    assert "CQ05" in questions
    assert "Functional Data Overreach" in questions["CQ05"].purpose


def test_purpose_compatibility_question_exists():
    questions = {
        question.id: question
        for question in FDO_COMPETENCY_QUESTIONS
    }

    assert "CQ07" in questions
    assert "purpose" in questions["CQ07"].question.lower()


def test_evidence_traceability_question_exists():
    questions = {
        question.id: question
        for question in FDO_COMPETENCY_QUESTIONS
    }

    assert "CQ20" in questions
    assert "evidence" in questions["CQ20"].question.lower()


def test_all_questions_have_purposes():
    for question in FDO_COMPETENCY_QUESTIONS:
        assert question.purpose


def test_all_questions_have_expected_results():
    for question in FDO_COMPETENCY_QUESTIONS:
        assert question.expected_result