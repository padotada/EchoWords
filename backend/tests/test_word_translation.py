import json
import pytest
import word_translation
from word_translation import (SegmentTranslationData, TranslationSegment, validate_translation)

def test_translation_segment_schema():
    segment = TranslationSegment(
        source="你好",
        translation="hello",
        type="text"
    )
    
    assert segment.source == "你好"
    assert segment.translation == "hello"
    assert segment.type == "text"
    
def test_segment_translation_schema():
    result = SegmentTranslationData(
        source_text="你好。",
        target_language="English",
        segments=[
            TranslationSegment(
                source="你好",
                translation="hello",
                type="text",
            ),
            TranslationSegment(
                source="。",
                translation="。",
                type="punctuation",
            ),
        ]
    )
    assert result.source_text == "你好。"
    assert result.target_language == "English"
    assert len(result.segments) == 2
    
def test_validate_translation_reconstructs_source():
    source = "你好，世界。"

    result = SegmentTranslationData(
        source_text=source,
        target_language="English",
        segments=[
            TranslationSegment(
                source="你好",
                translation="hello",
                type="text",
            ),
            TranslationSegment(
                source="，",
                translation="，",
                type="punctuation",
            ),
            TranslationSegment(
                source="世界",
                translation="world",
                type="text",
            ),
            TranslationSegment(
                source="。",
                translation="。",
                type="punctuation",
            ),
        ],
    )

    validate_translation(result, source)
    
def test_validate_translation_rejects_missing_source_text():
    source = "你好，世界。"

    result = SegmentTranslationData(
        source_text=source,
        target_language="English",
        segments=[
            TranslationSegment(
                source="你好",
                translation="hello",
                type="text",
            ),
            TranslationSegment(
                source="世界",
                translation="world",
                type="text",
            ),
            TranslationSegment(
                source="。",
                translation="。",
                type="punctuation",
            ),
        ],
    )

    with pytest.raises(
        ValueError,
        match="do not reconstruct"
    ):
        validate_translation(result, source)
        
def test_validate_translation_rejects_translated_punctuation():
    source = "你好。"

    result = SegmentTranslationData(
        source_text=source,
        target_language="English",
        segments=[
            TranslationSegment(
                source="你好",
                translation="hello",
                type="text",
            ),
            TranslationSegment(
                source="。",
                translation="period",
                type="punctuation",
            ),
        ],
    )

    with pytest.raises(ValueError):
        validate_translation(result, source)
        
def test_validate_translation_rejects_wrong_source_text():
    result = SegmentTranslationData(
        source_text="你好。",
        target_language="English",
        segments=[
            TranslationSegment(
                source="你好",
                translation="hello",
                type="text",
            ),
            TranslationSegment(
                source="。",
                translation="。",
                type="punctuation",
            ),
        ],
    )

    with pytest.raises(
        ValueError,
        match="doesn't match"
    ):
        validate_translation(
            result,
            "再见。"
        )
        
def test_validate_translation_rejects_modified_punctuation():
    source = "你好。"

    result = SegmentTranslationData(
        source_text=source,
        target_language="English",
        segments=[
            TranslationSegment(
                source="你好",
                translation="hello",
                type="text",
            ),
            TranslationSegment(
                source="。",
                translation="period",
                type="punctuation",
            ),
        ],
    )

    with pytest.raises(ValueError):
        validate_translation(result, source)


@pytest.mark.parametrize(
    "invalid_input",
    [
        "",
        "   ",
        "\n",
        "\t",
    ],
)
def test_word_translate_rejects_empty_input(
    invalid_input,
):
    with pytest.raises(ValueError):
        word_translation.word_translate(
            invalid_input
        )


def test_word_translate(mocker):
    source = "你好，世界。"

    fake_response = mocker.Mock()

    fake_response.text = json.dumps({
        "source_text": source,
        "target_language": "English",
        "segments": [
            {
                "source": "你好",
                "translation": "hello",
                "type": "text",
            },
            {
                "source": "，",
                "translation": "，",
                "type": "punctuation",
            },
            {
                "source": "世界",
                "translation": "world",
                "type": "text",
            },
            {
                "source": "。",
                "translation": "。",
                "type": "punctuation",
            },
        ],
    })

    mock_generate = mocker.patch.object(
        word_translation.client.models,
        "generate_content",
        return_value=fake_response,
    )

    result = word_translation.word_translate(
        source
    )

    assert isinstance(
        result,
        SegmentTranslationData,
    )

    assert result.source_text == source
    assert len(result.segments) == 4

    assert (
        result.segments[0].translation
        == "hello"
    )

    mock_generate.assert_called_once()


def test_word_translate_empty_response(mocker):
    fake_response = mocker.Mock()
    fake_response.text = None

    mocker.patch.object(
        word_translation.client.models,
        "generate_content",
        return_value=fake_response,
    )

    with pytest.raises(RuntimeError):
        word_translation.word_translate(
            "你好"
        )