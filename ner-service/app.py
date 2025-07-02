from flask import Flask, request, jsonify
from flask_cors import CORS
import spacy
import os

app = Flask(__name__)
CORS(app)

# Load the English NLP model
try:
    nlp = spacy.load("en_core_web_sm")
except:
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "NER API is running!"})

@app.route('/extract', methods=['POST'])
def extract_entities():
    text = request.json.get('text', '')
    doc = nlp(text)
    entities = [{'text': ent.text, 'label': ent.label_} for ent in doc.ents]
    return jsonify({"entities": entities})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
