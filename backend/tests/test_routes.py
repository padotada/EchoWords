import pytest
from app import app
from translate import FullTranslationData
from word_translation import SegmentTranslationData
from sentence_analysis import SentenceAnalysisData, SentenceAnalysis, SentenceComponent

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_translate_success(client, mocker):
    mock_result = FullTranslationData(
        source_text="你好",
        translation="Hello",
        source_language="Chinese",
        target_language="English",
    )

    mocker.patch(
        "app.translate.translate",
        return_value=mock_result,
    )

    response = client.post(
        "/api/translate",
        json={"text": "你好"},
    )
    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True
    assert data["error"] is None
    assert data["data"]["source_text"] == "你好"
    assert data["data"]["translation"] == "Hello"

def test_translate_rejects_empty_text(client):
    response = client.post(
        "/api/translate",
        json={"text": ""},
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["success"] is False
    assert data["data"] is None
    assert data["error"]["code"] == "EMPTY_TEXT"
    
def test_translate_rejects_whitespace(client):
    response = client.post(
        "/api/translate",
        json={"text": "   "},
    )

    assert response.status_code == 400
    
def test_translate_rejects_missing_text(client):
    response = client.post(
        "/api/translate",
        json={},
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["success"] is False
    assert data["error"]["code"] == "EMPTY_TEXT"
    
def test_translate_rejects_non_string_text(client):
    response = client.post(
        "/api/translate",
        json={"text": 123},
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["success"] is False
    assert data["error"]["code"] == "EMPTY_TEXT"
    
def test_analyze_sentence_success(client, mocker):
    mock_result = SentenceAnalysisData(
        source_text="我喜欢学习中文。",
        source_language="Chinese",
        target_language="English",
        sentences=[
            SentenceAnalysis(
            source="我喜欢学习中文。",
            translation="I like studying Chinese.",
            structure="Subject + Predicate + Object",
            explanation=(
            "我 is the subject, 喜欢 is the main verb, "
            "and 学习中文 functions as the object."
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
                )
            ]
            )
        ]
    )

    mocker.patch(
        "app.sentence_analysis.analyze_sentence",
        return_value=mock_result,
    )

    response = client.post(
        "/api/analyze/sentence",
        json={"text": "我喜欢学习中文。"},
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True
    assert data["data"]["source_text"] == "我喜欢学习中文。"
    assert data["data"]["target_language"] == "English"
    
def test_translate_segments_success(client, mocker):
    mock_result = SegmentTranslationData(
        source_text="你好",
        target_language="English",
        segments=[
            # valid TranslationSegment objects
        ],
    )

    mocker.patch(
        "app.word_translation.word_translate",
        return_value=mock_result,
    )

    response = client.post(
        "/api/translate/words",
        json={"text": "你好"},
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True
    assert data["data"]["source_text"] == "你好"
    
def test_translate_passes_text_to_service(client, mocker):
    mock_translate = mocker.patch(
        "app.translate.translate",
        return_value=FullTranslationData(
            source_text="你好",
            translation="Hello",
            source_language="Chinese",
            target_language="English",
        ),
    )

    client.post(
        "/api/translate",
        json={"text": "你好"},
    )

    mock_translate.assert_called_once_with("你好")
    
def test_empty_translation_does_not_call_service(client, mocker):
    mock_translate = mocker.patch(
        "app.translate.translate"
    )

    response = client.post(
        "/api/translate",
        json={"text": ""},
    )

    assert response.status_code == 400
    mock_translate.assert_not_called()