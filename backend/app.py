from flask import Flask, jsonify
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

# Build full path to questions.json based on this file's location
base_dir = os.path.dirname(os.path.abspath(__file__))
questions_file = os.path.join(base_dir, "questions.json")

# Load questions.json content
with open(questions_file, "r") as f:
    questions = json.load(f)

@app.route("/questions")
def get_questions():
    return jsonify(questions)

if __name__ == "__main__":
    app.run(debug=True)
