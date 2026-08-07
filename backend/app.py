from flask import Flask, jsonify, request
from flask.typing import ResponseReturnValue
from flask_cors import CORS
import translate
import word_translation
import sentence_analysis


app = Flask(__name__)
CORS(app)

@app.route('/api/translate', methods=["POST"])
def entire_translate()->ResponseReturnValue:
    data = request.data
    print(data.decode("utf-8"))
    if not data.strip():
        return jsonify({"error": "Request body cannot be empty"}), 400
    res = translate.translate(data.decode("utf-8"))
    if res is None:
        return jsonify({"error": "Translation failed"}), 500
    return res

    #return word_translate()

@app.route('/api/translate/words', methods=["POST"])
def s_translate():
    data = request.data
    res = sentence_analysis.analyze_sentence(data.decode("utf-8"))
    return res

@app.route('/api/analyze/sentence', methods=["POST"])
def w_translate():
    data = request.data
    print(data.decode("utf-8"))
    res = word_translation.word_translate(data.decode("utf-8"))
    print(res)
    return res

if __name__ == "__main__":
    app.run(debug=True)