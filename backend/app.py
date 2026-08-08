from flask import Flask, jsonify, request
from flask.typing import ResponseReturnValue
from flask_cors import CORS
import translate
import word_translation
import sentence_analysis


app = Flask(__name__)
CORS(app)

def is_valid_text(text: str):
    return isinstance(text, str) and bool(text.strip())

def error_response(code: str, message: str, status: int):
    return jsonify({
        "success": False,
        "data": None,
        "error": {
            "code": code,
            "message": message,
        },
    }), status

@app.post('/api/translate')
def translate_text()->ResponseReturnValue:
    data = request.get_json() or {}
    text = data.get("text", "")
    if not is_valid_text(text):
        return error_response("EMPTY_TEXT", "Text must not be empty", 400)
    translated_res = translate.translate(text)
    res = translated_res.model_dump()
    
    return jsonify({
        "success": True,
        "data": res,
        "error": None}), 200

@app.post('/api/analyze/sentence')
def analyze():
    data = request.get_json() or {}
    text = data.get("text", "")
    
    if not is_valid_text(text):
        return error_response("EMPTY_TEXT", "Text must not be empty", 400)
         
    analyzed_res = sentence_analysis.analyze_sentence(text)
    res = analyzed_res.model_dump()
         
    return jsonify({
        "success": True,
        "data": res,
        "error": None}), 200

@app.post('/api/translate/words')
def translate_segments():
    data = request.get_json() or {}
    text = data.get("text", "")
    
    if not is_valid_text(text):
        return error_response("EMPTY_TEXT", "Text must not be empty", 400)
         
    translated_res = word_translation.word_translate(text)
    res = translated_res.model_dump()
    
    return jsonify({
        "success": True,
        "data": res,
        "error": None}), 200

if __name__ == "__main__":
    app.run(debug=True)