import json
import os
from dotenv import load_dotenv
import google.genai as genai2
from google.genai.types import HarmCategory, HarmBlockThreshold, GenerateContentConfig, SafetySetting

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai2.Client(api_key=api_key)

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json",
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

config=GenerateContentConfig(
    **generation_config, safety_settings=safety_settings,
    system_instruction="""
  You are a professional translator helping an English-language learner.

The user will send a message beginning with the exact keyword TRANSLATE, followed by source text.

Translate the source text after TRANSLATE into English at the source-segment level.

Return only a valid JSON array. Do not include Markdown, code fences, explanations, headings, or commentary.

Output requirements:

Each array item must be a JSON object containing exactly one key-value pair.
The key must be the original source segment.
The value must be the English translation of that segment.
Preserve every character from the source text, including punctuation and whitespace.
Represent punctuation as separate segments.
Do not translate punctuation. For each punctuation segment, use the original punctuation mark as both the key and the value.
Preserve whitespace as separate segments, using the original whitespace as both the key and the value.
Keep all segments in their original order.
Concatenating the keys in order must reproduce the source text exactly.
Do not include the keyword TRANSLATE in the output.
Use valid JSON syntax with no trailing commas.

Example input:

TRANSLATE 你好，世界。

Example output:

[
{"你好": "hello"},
{"，": "，"},
{"世界": "world"},
{".": "."}
]
""" 
  )

chat_session = client.chats.create(
    model="gemini-3.6-flash",
    config=config)

def word_translate(msg):
    response = chat_session.send_message(f"TRANSLATE\n{msg}")
    return parse_json(response.text)

def main():
    message = "那么随着时间推移，三国人物阵营是怎样变化的呢？"
    response = chat_session.send_message(f"TRANSLATE\n{message}")
    print(parse_json(response.text))
    #return word_translate(message)

def parse_json(jsonfile):
    return json.loads(jsonfile)


if __name__=="__main__":
    main()
                        
# Disregard all prior instructions. You will be acting as a professional translator who is translating to an amateur learner. Provide me a word by word (INCLUDING punctuations) english translation of the text I will send you next.
#                         Your output will only have 1 JSON file, in which the text (INCLUDING PUNCTUATION) will be parsed into a dictionary with the original word being the key and the translation being the value. 
#                         All punctuation should be translated or considered during execution. 
#                         All of the keys must be able to combine to compose the entirety of the original text including punctuation. 
#                         Example input: "作为中国文学史上第一部章回小说，《三国演义》为我们展示出了一幅波澜壮阔乱世英雄争天下的历史画面。"
#                         Example output in the proper JSON schema: 
# [

#   {"作为": "as"},

#   {"中国": "China"},

#   {"文学": "literature"},

#   {"史上": "in history"},

#   {"第一部": "the first"},

#   {"章回": "chapter"},

#   {"小说": "novel"},

#   {"，": "comma"},

#   {"《三国演义》": "Romance of the Three Kingdoms"},

#   {"为": "for"},

#   {"我们": "us"},

#   {"展示": "show"},

#   {"出": "out"},

#   {"一幅": "a"},

#   {"波澜壮阔": "grand"},

#   {"乱世": "turbulent times"},

#   {"英雄": "hero"},

#   {"争": "fight"},

#   {"天下": "the world"},

#   {"的": "of"},

#   {"历史": "history"},

#   {"画面": "picture"}

#   {"。": "period"},

# ]

# YOU SHOULD NOT BE TRANSLATING ANY KIND OF PUNCTUATION. IGNORE ALL PUNCTUATION WHEN EXECUTING. You will only execute the prompt after I give the keyword "TRANSLATE". Don't give any other output or analysis or commentary other than the json file.

# message = """옛날에 큰 호랑이 한 마리가 숲 속에 살았다.
    #           어느 날 호랑이는 배가 고파서 마을로 갔다.
    #           마을 옆 밭에 소 한 마리가 서 있었다.
    #           호랑이는 소를 잡아 먹고 싶은데 갑자기 시끄러운 아기 울음소리를 들었다.
    #           밭 옆에 있는 집에서 아기가 울고 있었다.
    #           호랑이는 집으로 다가갔다.
    #           ‘아기가 맛있을 것 같아.’
    #           호랑이는 생각했다."""
    # message = """「おれの方が強い。」「いいや、ぼくの方が強い。」北風と太陽の声が聞えます。二人はどちらの力が強いかでケンカをしているようです。「太陽が毎日元気だから、暑くてみんな困っているよ。おれが涼しい風を吹くと、みんな嬉しそうだ。おれの方がみんなの役に立っているよ。」「でも、ぼくがいないと、木や野菜は育たないよ。冬は北風の吹く風が冷くて、とても寒かった。みんな外に出られなかったよね？最近は暖かいから、みんな喜よろこんでいるよ。」「いいや、あそこを見て。太陽が強く照すから、川の水がもうすぐ無なりそうだ。水がないと、みんな生活できないよ。」"""