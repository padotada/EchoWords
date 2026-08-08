import json

import pytest

import sentence_analysis
from sentence_analysis import (
    SentenceComponent,
    SentenceAnalysis,
    SentenceAnalysisData,
    validate_analysis,
)


SOURCE = "我喜欢学习中文。"


def make_valid_result() -> SentenceAnalysisData:
    """Create a valid sentence-analysis result for reuse in tests."""

    return SentenceAnalysisData(
        source_text=SOURCE,
        source_language="Chinese",
        target_language="English",
        sentences=[
            SentenceAnalysis(
                source=SOURCE,
                translation="I like studying Chinese.",
                structure="Subject + Predicate + Object",
                explanation=(
                    "The sentence uses 我 as the subject, 喜欢 as "
                    "the main verb, and 学习中文 as its object."
                ),
                components=[
                    SentenceComponent(
                        source="我",
                        translation="I",
                        role="subject",
                        part_of_speech="pronoun",
                    ),
                    SentenceComponent(
                        source="喜欢",
                        translation="like",
                        role="predicate",
                        part_of_speech="verb",
                    ),
                    SentenceComponent(
                        source="学习中文",
                        translation="studying Chinese",
                        role="object",
                        part_of_speech="verb phrase",
                    ),
                ],
            )
        ],
    )


def test_sentence_component_schema():
    component = SentenceComponent(
        source="我",
        translation="I",
        role="subject",
        part_of_speech="pronoun",
    )

    assert component.source == "我"
    assert component.translation == "I"
    assert component.role == "subject"
    assert component.part_of_speech == "pronoun"


def test_sentence_analysis_schema():
    result = make_valid_result()

    assert result.source_text == SOURCE
    assert result.source_language == "Chinese"
    assert result.target_language == "English"
    assert len(result.sentences) == 1

    sentence = result.sentences[0]

    assert sentence.source == SOURCE
    assert sentence.translation == "I like studying Chinese."
    assert len(sentence.components) == 3

def test_validate_analysis_accepts_valid_result():
    result = make_valid_result()
    validate_analysis(result, SOURCE)

def test_validate_analysis_rejects_wrong_source_text():
    result = make_valid_result()

    result.source_text = "错误的文本。"

    with pytest.raises(
        ValueError,
        match="does not match",
    ):
        validate_analysis(result, SOURCE)


def test_validate_analysis_rejects_no_sentences():
    result = SentenceAnalysisData(
        source_text=SOURCE,
        source_language="Chinese",
        target_language="English",
        sentences=[],
    )

    with pytest.raises(
        ValueError,
        match="no sentence analysis",
    ):
        validate_analysis(result, SOURCE)


def test_validate_analysis_rejects_empty_sentence_source():
    result = make_valid_result()

    result.sentences[0].source = ""

    with pytest.raises(ValueError):
        validate_analysis(result, SOURCE)


def test_validate_analysis_rejects_empty_translation():
    result = make_valid_result()

    result.sentences[0].translation = ""

    with pytest.raises(ValueError):
        validate_analysis(result, SOURCE)


def test_validate_analysis_rejects_empty_structure():
    result = make_valid_result()

    result.sentences[0].structure = ""

    with pytest.raises(ValueError):
        validate_analysis(result, SOURCE)


def test_validate_analysis_rejects_empty_explanation():
    result = make_valid_result()

    result.sentences[0].explanation = ""

    with pytest.raises(ValueError):
        validate_analysis(result, SOURCE)

@pytest.mark.parametrize(
    "invalid_input",
    [
        "",
        " ",
        "   ",
        "\n",
        "\t",
    ],
)
def test_analyze_sentence_rejects_empty_input(invalid_input):
    with pytest.raises(
        ValueError,
        match="non-empty",
    ):
        sentence_analysis.analyze_sentence(invalid_input)


def test_analyze_sentence_returns_valid_result(mocker):
    fake_response = mocker.Mock()

    fake_response.text = json.dumps(
        {
            "source_text": SOURCE,
            "source_language": "Chinese",
            "target_language": "English",
            "sentences": [
                {
                    "source": SOURCE,
                    "translation": "I like studying Chinese.",
                    "structure": "Subject + Predicate + Object",
                    "explanation": (
                        "我 is the subject, 喜欢 is the main verb, "
                        "and 学习中文 functions as the object."
                    ),
                    "components": [
                        {
                            "source": "我",
                            "translation": "I",
                            "role": "subject",
                            "part_of_speech": "pronoun",
                        },
                        {
                            "source": "喜欢",
                            "translation": "like",
                            "role": "predicate",
                            "part_of_speech": "verb",
                        },
                        {
                            "source": "学习中文",
                            "translation": "studying Chinese",
                            "role": "object",
                            "part_of_speech": "verb phrase",
                        },
                    ],
                }
            ],
        },
        ensure_ascii=False,
    )

    mock_generate = mocker.patch.object(
        sentence_analysis.client.models,
        "generate_content",
        return_value=fake_response,
    )

    result = sentence_analysis.analyze_sentence(SOURCE)

    assert isinstance(result, SentenceAnalysisData)
    assert result.source_text == SOURCE
    assert result.target_language == "English"
    assert len(result.sentences) == 1

    sentence = result.sentences[0]

    assert sentence.translation == "I like studying Chinese."
    assert len(sentence.components) == 3
    assert sentence.components[0].source == "我"
    assert sentence.components[0].role == "subject"

    mock_generate.assert_called_once()


def test_analyze_sentence_rejects_empty_gemini_response(mocker):
    fake_response = mocker.Mock()
    fake_response.text = None

    mocker.patch.object(
        sentence_analysis.client.models,
        "generate_content",
        return_value=fake_response,
    )

    with pytest.raises(
        RuntimeError,
        match="empty response",
    ):
        sentence_analysis.analyze_sentence(SOURCE)


def test_analyze_sentence_rejects_invalid_json(mocker):
    fake_response = mocker.Mock()
    fake_response.text = "this is not valid JSON"

    mocker.patch.object(
        sentence_analysis.client.models,
        "generate_content",
        return_value=fake_response,
    )

    with pytest.raises(Exception):
        sentence_analysis.analyze_sentence(SOURCE)


def test_analyze_sentence_rejects_invalid_schema(mocker):
    fake_response = mocker.Mock()

    fake_response.text = json.dumps(
        {
            "source_text": SOURCE,
            "target_language": "English",
        },
        ensure_ascii=False,
    )

    mocker.patch.object(
        sentence_analysis.client.models,
        "generate_content",
        return_value=fake_response,
    )

    with pytest.raises(Exception):
        sentence_analysis.analyze_sentence(SOURCE)