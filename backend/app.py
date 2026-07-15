from flask import Flask, request
from flask_cors import CORS
import translate
import word_translation
import sentence_analysis
import json


app = Flask(__name__)
CORS(app)

@app.route('/tran', methods=["POST"])
def entire_translate():
    data = request.data
    print(data.decode("utf-8"))
    res = (translate.translate(data.decode("utf-8")))
    return res

    #return word_translate()

@app.route('/stran', methods=["POST"])
def s_translate():
    data = request.data
    res = (sentence_analysis.sentence_translate(data.decode("utf-8")))
    return res

@app.route('/wtran', methods=["POST"])
def w_translate():
    data = request.data
    print(data.decode("utf-8"))
    res = (word_translation.word_translate(data.decode("utf-8")))
    print(res)
    return res

if __name__ == "__main__":
    app.run(debug=True)