import os
from typing import Literal
from dotenv import load_dotenv
import google.genai as genai2
from google.genai.types import HarmCategory, HarmBlockThreshold, GenerateContentConfig, SafetySetting
from pydantic import BaseModel, Field

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai2.Client(api_key=api_key)

class TranslationSegment(BaseModel):
    source: str = Field(
        description="The exact source segment from the original text."
    )
    translation: str = Field(
        description="The English translation of the source segment"
    )
    type: Literal["text", "punctuation", "whitespace"]
    
class SegmentTranslationData(BaseModel):
    source_text: str
    target_language: str
    segments: list[TranslationSegment]

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

config=GenerateContentConfig(
    temperature=0.2,
    top_p=0.9,
    max_output_tokens=8192,
    response_mime_type="application/json",
    response_schema=SegmentTranslationData,
    safety_settings=safety_settings,
    system_instruction="""
  You are a professional translator helping an English-language learner.

Translate the supplied source text into English at the source-segment level.

Segmentation rules:

- Use type "text" for words, phrases, characters, names, or other meaningful
  lexical units.
- Use type "punctuation" for punctuation marks.
- Use type "whitespace" for spaces, tabs, and newline characters.
- Preserve all source segments in their original order.
- Concatenating every source field must reproduce the original text exactly.
- Translate only segments whose type is "text".
- For punctuation and whitespace, copy the source value unchanged into the
  translation field.
- Do not omit, reorder, or invent source characters.
- target_language must be "English".
- source_text must exactly match the user's supplied text.
""" 
  )

def word_translate(msg: str)->SegmentTranslationData:
    if not isinstance(msg, str) or not msg.strip():
        raise ValueError("Source text must be a non empty string.")
    
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=msg,
        config=config
    )
    
    if response.text is None:
        raise RuntimeError("Gemini returned an empty response.")
    result = SegmentTranslationData.model_validate_json(
        response.text
    )
    validate_translation(result, msg)
    return result

def validate_translation(result: SegmentTranslationData, original_text: str)->None:
    if result.source_text != original_text:
        raise ValueError("Gemini returned a source text that doesn't match the input.")
    reconstructed = "".join(segment.source for segment in result.segments)
    if reconstructed != original_text:
        raise ValueError("Translation segments do not reconstruct the original text.")
    
    for segment in result.segments:
        if segment.type in {"punctuation", "whitespace"}:
            if segment.translation != segment.source:
                raise ValueError(f"{segment.type} was modified: "
                    f"{segment.source!r}") # raw text
    
def main():
    message = "那么随着时间推移，三国人物阵营是怎样变化的呢？"
    res = word_translate(message)
    print(res.model_dump_json(indent=2))

if __name__=="__main__":
    main()
                        


