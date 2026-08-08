import json
import os
from typing import Literal
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import google.genai as genai
from google.genai.types import HarmCategory, HarmBlockThreshold, GenerateContentConfig, SafetySetting

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

class SentenceComponent(BaseModel):
  source: str = Field(description="The exact source text for this grammatical component.")
  translation: str = Field(description="The English translation of this component.")
  role: str = Field(description="The grammatical role of the component, such as subject, predicate, object, modifier, or complement.")
  part_of_speech: str = Field(description="The primary grammatical category of the component such as noun, verb, pronoun, adjective, or phrase.")
  
class SentenceAnalysis(BaseModel):
  source: str = Field(
        description="The exact original sentence being analyzed."
    )

  translation: str = Field(
      description="A natural English translation of the sentence."
  )

  structure: str = Field(
      description=(
          "A concise representation of the sentence's grammatical structure."
      )
  )

  explanation: str = Field(
      description=(
          "A learner-friendly explanation of how the sentence is constructed."
      )
  )

  components: list[SentenceComponent]
  
class SentenceAnalysisData(BaseModel):
  source_text: str = Field(
      description="The exact source text supplied by the user."
  )
  source_language: str = Field(
      description="The detected language of the source text."
  )
  target_language: Literal["English"]
  sentences: list[SentenceAnalysis]

safety_settings=[SafetySetting(category=HarmCategory.HARM_CATEGORY_HATE_SPEECH, threshold=HarmBlockThreshold.BLOCK_NONE),
                   SafetySetting(category=HarmCategory.HARM_CATEGORY_HARASSMENT, threshold=HarmBlockThreshold.BLOCK_NONE),
                   SafetySetting(category=HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, threshold=HarmBlockThreshold.BLOCK_NONE),
                   SafetySetting(category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, threshold=HarmBlockThreshold.BLOCK_NONE)
]

config = GenerateContentConfig(
  temperature=0.2,
  top_p=0.9,
  max_output_tokens=8192,
  response_mime_type="application/json", 
  response_schema=SentenceAnalysisData,
  safety_settings=safety_settings,
  system_instruction = 
  """You are a professional language analyst and translator helping an English-language learner.

Analyze the supplied source text sentence by sentence.

For each sentence:

Preserve the exact original sentence in the source field.
Provide a natural English translation that preserves the original meaning, tone, and structure as closely as possible.
Describe the grammatical structure in clear, concise English.
Provide a learner-friendly explanation of how the sentence is constructed and what the sentence is doing in context.
Break the sentence into meaningful grammatical components.
For each component, preserve the exact source text, provide its English translation, identify its grammatical role, and identify its part of speech or phrase type.

General rules:

- Analyze every sentence in the supplied text.
- Preserve sentence order.
- Do not omit source text.
- Do not invent information that is not present in the source.
- Use clear terminology suitable for a learner.
- Keep grammatical explanations specific to the actual sentence rather than giving generic grammar descriptions.
- The source_text field must exactly match the user's supplied text.
- Detect and report the source language.
- The target language must be English.
"""
)

def analyze_sentence(original_text: str)->SentenceAnalysisData:
    if not isinstance(original_text, str) or not original_text.strip():
      raise ValueError("Source text must be a non-empty string.")
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=original_text,
        config=config,
    )
    if response.text is None:
      raise RuntimeError("Gemini returned an empty response.")
    result = SentenceAnalysisData.model_validate_json(response.text)
    validate_analysis(result, original_text)
    return result

def validate_analysis(result: SentenceAnalysisData, original_text: str)->None:
  if result.source_text != original_text:
    raise ValueError("Gemini returned source_text that does not match the input.")
  if not result.sentences:
    raise ValueError("Gemini returned no sentence analysis.")
  
  for sentence in result.sentences:
    if not sentence.source.strip():
      raise ValueError("Sentence analysis contains an empty source sentence.")
    if not sentence.translation.strip():
      raise ValueError("Sentence analysis contains an empty translation.")
    if not sentence.structure.strip():
      raise ValueError("Sentence analysis contains an empty structure.")
    if not sentence.explanation.strip():
      raise ValueError("Sentence analysis contains an empty explanation.")
    
def main():
    message = "作为中国文学史上第一部章回小说，《三国演义》为我们展示出了一幅波澜壮阔乱世英雄争天下的历史画面，故事情节随着几大人物阵营的演变紧紧抓牢看客眼球。那么随着时间推移，三国人物阵营是怎样变化的呢？狗熊会根据《三国演义》原著电子版汉语文本，应用文本分析、关联规则挖掘和社区探测技术，从数据角度分析三国各个时期的人物阵营情况。"
    result = analyze_sentence(message)
    print(result.model_dump_json(indent=2, ensure_ascii=False))
    
if __name__ == "__main__":
    main()
    

    