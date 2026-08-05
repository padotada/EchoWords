import json
import os
from dotenv import load_dotenv
import google.genai as genai
from google.genai.types import HarmCategory, HarmBlockThreshold

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
  model_name="gemini-3.6-flash",
  generation_config=generation_config,
  system_instruction = """Disregard all previous prompts. You will be acting as a professional translator who is translating to an amateur learner. Do not respond until I prompt you. 
                          I will later provide lines of text for you in a language. 
                          Analyze the grammar and the sentence structure in detail line by line for every sentence. 
                          After analyzing, give the direct translation. Please respond back in English that still reflects the original tone and structure. 
                          Put the response of your analysis in English in JSON format. Even for the nested key value pairs, recursively change the key into English. 
                          Also for each of the words and/or phrases from the original language, put a corresponding English word/phrase by recursively adding English next to the original language. 
                          Use this JSON schema: 
                          {Sentence: “original sentence”, Translation: “translated sentence”, Grammatical structure: “grammar”, Analysis: “translated analysis of the entire sentence, not individual words” }
                          Return: list[dictionaries] 

                          Example input: "作为中国文学史上第一部章回小说，《三国演义》为我们展示出了一幅波澜壮阔乱世英雄争天下的历史画面，故事情节随着几大人物阵营的演变紧紧抓牢看客眼球。那么随着时间推移，三国人物阵营是怎样变化的呢？狗熊会根据《三国演义》原著电子版汉语文本，应用文本分析、关联规则挖掘和社区探测技术，从数据角度分析三国各个时期的人物阵营情况。"

                          Example output:
                          [
                            {
                              "Sentence": "作为中国文学史上第一部章回小说，《三国演义》为我们展示出了一幅波澜壮阔乱世英雄争天下的历史画面，故事情节随着几大人物阵营的演变紧紧抓牢看客眼球。", 
                              "Translation": "As the first chapter novel in the history of Chinese literature, \"Romance of the Three Kingdoms\" presents us with a magnificent historical picture of heroes vying for supremacy in a turbulent world. The plot, with the constant evolution of the major character camps, firmly captivates the audience.", 
                              "Grammatical structure": "Complex sentence, containing multiple parallel clauses and adverbial clauses. The subject is \"《三国演义》\" (Romance of the Three Kingdoms), and the predicates are \"展示\" (present) and \"抓牢\" (captivate).", 
                              "Analysis": "This sentence uses multiple parallel clauses and adverbial clauses to comprehensively describe the characteristics of \"Romance of the Three Kingdoms\" as a literary work and its appeal to readers." 
                            },
                            {
                              "Sentence": "那么随着时间推移，三国人物阵营是怎样变化的呢？", 
                              "Translation": "So, how did the character camps in the Three Kingdoms change over time?", 
                              "Grammatical structure": "Interrogative sentence, the subject is \"三国人物阵营\" (character camps in the Three Kingdoms), and the predicate is \"变化\" (change).", 
                              "Analysis": "This sentence poses the research question and introduces the research content." 
                            },
                            {
                              "Sentence": "狗熊会根据《三国演义》原著电子版汉语文本，应用文本分析、关联规则挖掘和社区探测技术，从数据角度分析三国各个时期的人物阵营情况。", 
                              "Translation": "Gou Xiong will analyze the electronic text version of the original \"Romance of the Three Kingdoms\" using text analysis, association rule mining, and community detection techniques to examine the character camp situations in various periods of the Three Kingdoms from a data perspective.", 
                              "Grammatical structure": "Simple sentence, the subject is \"狗熊会\" (Gou Xiong), and the predicate is \"分析\" (analyze).", 
                              "Analysis": "This sentence describes the research methodology and data source used in the study." 
                            }
                          ]


                          You should respond back in English and only the JSON file with the correct return format when I say PLEASE HELP. DO NOT ADD ANY ADDITIONAL COMMENTARY BESIDES THE JSON FILE.
                          """,
  safety_settings={HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                   HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                   HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                   HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                   }
)

chat_session = model.start_chat(
  history=[
  ]
)

def sentence_translate(original_text: str):
    response = chat_session.send_message(original_text)
    response = chat_session.send_message("PLEASE HELP")
    return parse_json(response.text)
    
def main():
    #message = "作为中国文学史上第一部章回小说，《三国演义》为我们展示出了一幅波澜壮阔乱世英雄争天下的历史画面，故事情节随着几大人物阵营的演变紧紧抓牢看客眼球。那么随着时间推移，三国人物阵营是怎样变化的呢？狗熊会根据《三国演义》原著电子版汉语文本，应用文本分析、关联规则挖掘和社区探测技术，从数据角度分析三国各个时期的人物阵营情况。"
    message = """"""
    response = chat_session.send_message(message)
    response = chat_session.send_message("PLEASE HELP")
    print(parse_json(response.text))


def parse_json(some_file):
    return json.loads(some_file)

if __name__ == "__main__":
    main()
    

    