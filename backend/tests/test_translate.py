import json

import pytest
from pydantic import ValidationError

import translate
from translate import FullTranslationData


class FakeResponse:
    def __init__(self, text):
        self.text = text


def make_translation_json(
    source_text="안녕하세요.",
    translation="Hello.",
    source_language="Korean",
    target_language="English",
):
    return json.dumps(
        {
            "source_text": source_text,
            "translation": translation,
            "source_language": source_language,
            "target_language": target_language,
        }
    )


def test_translate_returns_full_translation_data(monkeypatch):
    source = "안녕하세요."

    def fake_generate_content(*, model, contents, config):
        assert contents == source
        return FakeResponse(
            make_translation_json(
                source_text=source,
                translation="Hello.",
                source_language="Korean",
            )
        )

    monkeypatch.setattr(
        translate.client.models,
        "generate_content",
        fake_generate_content,
    )

    result = translate.translate(source)

    assert isinstance(result, FullTranslationData)
    assert result.source_text == source
    assert result.translation == "Hello."
    assert result.source_language == "Korean"
    assert result.target_language == "English"


@pytest.mark.parametrize(
    "invalid_input",
    [
        "",
        "   ",
        "\n\t",
        None,
        123,
    ],
)
def test_translate_rejects_invalid_input(invalid_input):
    with pytest.raises(
        ValueError,
        match="Source text must be a non-empty string",
    ):
        translate.translate(invalid_input)


def test_translate_raises_when_gemini_returns_none(monkeypatch):
    def fake_generate_content(*, model, contents, config):
        return FakeResponse(None)

    monkeypatch.setattr(
        translate.client.models,
        "generate_content",
        fake_generate_content,
    )

    with pytest.raises(
        RuntimeError,
        match="Gemini returned an empty response",
    ):
        translate.translate("안녕하세요.")


def test_translate_rejects_invalid_json(monkeypatch):
    def fake_generate_content(*, model, contents, config):
        return FakeResponse("this is not valid JSON")

    monkeypatch.setattr(
        translate.client.models,
        "generate_content",
        fake_generate_content,
    )

    with pytest.raises(ValidationError):
        translate.translate("안녕하세요.")


def test_translate_rejects_missing_required_fields(monkeypatch):
    source = "안녕하세요."

    incomplete_json = json.dumps(
        {
            "source_text": source,
            "translation": "Hello.",
        }
    )

    def fake_generate_content(*, model, contents, config):
        return FakeResponse(incomplete_json)

    monkeypatch.setattr(
        translate.client.models,
        "generate_content",
        fake_generate_content,
    )

    with pytest.raises(ValidationError):
        translate.translate(source)


def test_translate_rejects_changed_source_text(monkeypatch):
    source = "안녕하세요."

    def fake_generate_content(*, model, contents, config):
        return FakeResponse(
            make_translation_json(
                source_text="Different source text",
                translation="Hello.",
            )
        )

    monkeypatch.setattr(
        translate.client.models,
        "generate_content",
        fake_generate_content,
    )

    with pytest.raises(
        ValueError,
        match="doesn't match the input",
    ):
        translate.translate(source)


def test_translate_rejects_wrong_target_language(monkeypatch):
    source = "안녕하세요."

    def fake_generate_content(*, model, contents, config):
        return FakeResponse(
            make_translation_json(
                source_text=source,
                translation="Bonjour.",
                target_language="French",
            )
        )

    monkeypatch.setattr(
        translate.client.models,
        "generate_content",
        fake_generate_content,
    )

    with pytest.raises(
        ValueError,
        match="Unexpected target language",
    ):
        translate.translate(source)


@pytest.mark.parametrize(
    "empty_translation",
    [
        "",
        "   ",
        "\n\t",
    ],
)
def test_translate_rejects_empty_translation(
    monkeypatch,
    empty_translation,
):
    source = "안녕하세요."

    def fake_generate_content(*, model, contents, config):
        return FakeResponse(
            make_translation_json(
                source_text=source,
                translation=empty_translation,
            )
        )

    monkeypatch.setattr(
        translate.client.models,
        "generate_content",
        fake_generate_content,
    )

    with pytest.raises(
        ValueError,
        match="Gemini returned an empty translation",
    ):
        translate.translate(source)


def test_validate_translation_accepts_valid_result():
    source = "안녕하세요."

    result = FullTranslationData(
        source_text=source,
        translation="Hello.",
        source_language="Korean",
        target_language="English",
    )

    translate.validate_translation(result, source)


def test_source_language_may_be_none():
    result = FullTranslationData(
        source_text="你好。",
        translation="Hello.",
        source_language=None,
        target_language="English",
    )

    assert result.source_language is None