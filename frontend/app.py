from flask import Flask, request, jsonify
from flask_cors import CORS
from translate import your_translate_function, your_analysis_function

app = Flask(__name__)
CORS(app)  # Allows cross-origin requests from your React frontend

@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.json  # Get JSON data from POST request
    text = data.get('text', '')  # Get the text to translate
    translated_text = your_translate_function(text)  # Call your function
    return jsonify({"translated_text": translated_text})

@app.route('/analyze', methods=['POST'])
def analyze_text():
    data = request.json
    text = data.get('text', '')
    analysis = your_analysis_function(text)  # Call your function
    return jsonify(analysis)  # Return the analysis as JSON

if __name__ == '__main__':
    app.run(debug=True)
