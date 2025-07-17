from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import random
import json
import os

app = Flask(__name__, static_folder='../static', static_url_path='/')

CORS(app)

# Load fallback questions from questions.json
with open("questions.json", "r") as f:
    fallback_questions = json.load(f)

@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/images/<path:filename>')
def serve_images(filename):
    return send_from_directory(os.path.join(app.static_folder, 'images'), filename)

@app.route('/questions', methods=['GET'])
def get_questions():
    primary = request.args.get('primary')
    secondary = request.args.get('secondary')
    if not primary or not secondary:
        return jsonify({"error": "Missing primary or secondary position"}), 400

    # Filter questions by positions
    filtered = [q for q in fallback_questions if q["position"].lower() in [primary.lower(), secondary.lower()]]

    # Choose 25 random questions
    if len(filtered) < 25:
        questions = random.sample(filtered, len(filtered))
    else:
        questions = random.sample(filtered, 25)

    return jsonify(questions)

if __name__ == '__main__':
    app.run(debug=True)
