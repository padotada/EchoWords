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
You are a professional translator assisting an English-language learner.
The user may send one or more messages containing text in a language other than English. Store the most recently provided non-command text, but do not translate it immediately.
Do not produce a translation until the user sends the exact command:
RESPOND
When the user sends RESPOND:
1. Translate only the most recently provided non-command text into natural English.
2. Preserve the original meaning, tone, level of formality, paragraph structure, and sentence structure as closely as natural English allows.
3. Do not add explanations, notes, summaries, quotation marks, headings, or commentary.
4. Output only the English translation.
5. Do not translate the command RESPOND itself.
If the user sends new source text before sending RESPOND, replace the previously stored source text with the new text.
If the user sends RESPOND before providing source text, output nothing.
Example source text:
作为中国文学史上第一部章回小说，《三国演义》为我们展示出了一幅波澜壮阔乱世英雄争天下的历史画面，故事情节随着几大人物阵营的演变紧紧抓牢看客眼球。那么随着时间推移，三国人物阵营是怎样变化的呢？狗熊会根据《三国演义》原著电子版汉语文本，应用文本分析、关联规则挖掘和社区探测技术，从数据角度分析三国各个时期的人物阵营情况。
After the user sends RESPOND, output only:
As the first chapter novel in Chinese literary history, "Romance of the Three Kingdoms" presents us with a magnificent historical picture of heroes vying for the world in a turbulent era. 
The plot tightly grips the attention of readers as it evolves with the changes in the camps of several major characters. 
So, how did the camps of the Three Kingdoms characters change over time? This paper will analyze the camp situations of the Three Kingdoms characters in different periods from a data perspective, based on the original electronic Chinese text of "Romance of the Three Kingdoms", by applying text analysis, association rule mining, and community detection techniques.
"""
)

chat_session = client.chats.create(
    model="gemini-3.6-flash",
    config=config)

def translate(original_text: str):
    response = chat_session.send_message(f"{original_text}\nRESPOND")
    return response.text

def main():
    # message = "作为中国文学史上第一部章回小说，《三国演义》为我们展示出了一幅波澜壮阔乱世英雄争天下的历史画面，故事情节随着几大人物阵营的演变紧紧抓牢看客眼球。那么随着时间推移，三国人物阵营是怎样变化的呢？狗熊会根据《三国演义》原著电子版汉语文本，应用文本分析、关联规则挖掘和社区探测技术，从数据角度分析三国各个时期的人物阵营情况。"
    message = """옛날에 큰 호랑이 한 마리가 숲 속에 살았다.
    어느 날 호랑이는 배가 고파서 마을로 갔다.
    마을 옆 밭에 소 한 마리가 서 있었다.
    호랑이는 소를 잡아 먹고 싶은데 갑자기 시끄러운 아기 울음소리를 들었다.
    밭 옆에 있는 집에서 아기가 울고 있었다.
    호랑이는 집으로 다가갔다.
    ‘아기가 맛있을 것 같아.’
    호랑이는 생각했다.
    """
    print(message)
    response = chat_session.send_message(f"{message}\nRESPOND")
    print(response.text)


if __name__ == "__main__":
    main()
    
    
