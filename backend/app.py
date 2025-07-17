from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os
import json

app = Flask(__name__, static_folder="../static", static_url_path="")
CORS(app)

# Load questions.json
with open(os.path.join(os.path.dirname(__file__), "questions.json"), "r") as f:
    questions = json.load(f)

@app.route("/questions")
def get_questions():
    return jsonify(questions)

@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(app.static_folder, path)
