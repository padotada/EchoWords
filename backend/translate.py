from typing import Literal
from pydantic import BaseModel, Field
import google.genai as genai3
from google.genai.types import HarmCategory, HarmBlockThreshold, GenerateContentConfig, SafetySetting
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai3.Client(api_key=api_key)

class FullTranslationData(BaseModel):
    source_text: str = Field(
        description="The exact source text supplied by the user."
    )
    translation: str = Field(
        description="The complete English translation of the source text."
    )
    source_language: str | None = Field(
        default=None,
        description="The detected language of the source text."
    )
    target_language: str = Field(
        description='The target language. Must be "English".'
    )


safety_settings = [
    SafetySetting(
        category= HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=HarmBlockThreshold.BLOCK_NONE,
    ),
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=HarmBlockThreshold.BLOCK_NONE,
    ),
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=HarmBlockThreshold.BLOCK_NONE,
    ),
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=HarmBlockThreshold.BLOCK_NONE,
    ),
]

config = GenerateContentConfig(
    temperature=0.2,
    top_p=0.9,
    max_output_tokens=8192,
    response_mime_type="application/json",
    response_schema=FullTranslationData,
    safety_settings=safety_settings,
    system_instruction = """
You are a professional translator assisting an English-language learner.

Translate the supplied source text into natural English.

Translation rules:

- Preserve the original meaning and tone.
- Preserve the level of formality.
- Preserve paragraph structure as closely as natural English allows.
- Preserve sentence structure where doing so produces natural English.
- Do not add explanations, notes, summaries, headings, or commentary.
- source_text must exactly match the user's supplied text.
- translation must contain only the English translation.
- source_language should identify the language of the supplied text.
- target_language must be "English".
"""
)

def translate(original_text: str)->FullTranslationData:
    if not isinstance(original_text, str) or not original_text.strip():
        raise ValueError("Source text must be a non-empty string.")

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=original_text,
        config=config,
    )
    
    if response.text is None:
        raise RuntimeError("Gemini returned an empty response.")
    
    result = FullTranslationData.model_validate_json(response.text)
    validate_translation(result, original_text)
    return result

def validate_translation( result: FullTranslationData, original_text: str) -> None:
    if result.source_text != original_text:
        raise ValueError(
            "Gemini returned source text that doesn't match the input."
        )

    if result.target_language != "English":
        raise ValueError(
            f"Unexpected target language: {result.target_language!r}"
        )

    if not result.translation.strip():
        raise ValueError("Gemini returned an empty translation.")

def main():
    message = """옛날에 큰 호랑이 한 마리가 숲 속에 살았다.
    어느 날 호랑이는 배가 고파서 마을로 갔다.
    마을 옆 밭에 소 한 마리가 서 있었다.
    호랑이는 소를 잡아 먹고 싶은데 갑자기 시끄러운 아기 울음소리를 들었다.
    밭 옆에 있는 집에서 아기가 울고 있었다.
    호랑이는 집으로 다가갔다.
    ‘아기가 맛있을 것 같아.’
    호랑이는 생각했다.
    """
    result = translate(message)
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
    
    
