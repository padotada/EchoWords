import google.genai as genai3
from google.genai.types import HarmCategory, HarmBlockThreshold, GenerateContentConfig, SafetySetting
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai3.Client(api_key=api_key)
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

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
  **generation_config, safety_settings=safety_settings,
  system_instruction = 
  """
  Disregard all previous prompts. You will be acting as a professional translator who is translating for an amateur learner. 
  Do not respond until I say "RESPOND". I will provide lines of text for you to translate in a foreign language. 
  DO NOT perform the translation when the foreign laguage text is provided.
  ONLY WHEN prompted with the word "RESPOND," provide the translated text in English and NOTHING ELSE. DO NOT TRANSLATE UNLESS I type "RESPOND".
  Make sure that the english translated version still reflects the original tone and structure. 
  When prompted, do not provide anything else EXCEPT for the translated English version of the original text.
  Example input: "作为中国文学史上第一部章回小说，《三国演义》为我们展示出了一幅波澜壮阔乱世英雄争天下的历史画面，故事情节随着几大人物阵营的演变紧紧抓牢看客眼球。那么随着时间推移，三国人物阵营是怎样变化的呢？狗熊会根据《三国演义》原著电子版汉语文本，应用文本分析、关联规则挖掘和社区探测技术，从数据角度分析三国各个时期的人物阵营情况。"
  Example ouput: "As the first chapter novel in Chinese literary history, "Romance of the Three Kingdoms" presents us with a magnificent historical picture of heroes vying for the world in a turbulent era. The plot tightly grips the attention of readers as it evolves with the changes in the camps of several major characters. So, how did the camps of the Three Kingdoms characters change over time? This paper will analyze the camp situations of the Three Kingdoms characters in different periods from a data perspective, based on the original electronic Chinese text of "Romance of the Three Kingdoms", by applying text analysis, association rule mining, and community detection techniques."
  When prompted with "RESPOND", execute the translation on the last given piece of text other than "RESPOND".
  """
)

chat_session = client.chats.create(
    model="gemini-3.6-flash",
    config=config)

def translate(original_text: str):
    response = chat_session.send_message(original_text)
    response = chat_session.send_message("RESPOND")
    return response.text

def main():
    message = "作为中国文学史上第一部章回小说，《三国演义》为我们展示出了一幅波澜壮阔乱世英雄争天下的历史画面，故事情节随着几大人物阵营的演变紧紧抓牢看客眼球。那么随着时间推移，三国人物阵营是怎样变化的呢？狗熊会根据《三国演义》原著电子版汉语文本，应用文本分析、关联规则挖掘和社区探测技术，从数据角度分析三国各个时期的人物阵营情况。"
    print(message)
    response = chat_session.send_message(message)
    response = chat_session.send_message("RESPOND")
    print(response.text)


if __name__ == "__main__":
    main()
    
    
