from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os
import json

# Setup app to serve from /static
app = Flask(__name__, static_folder="../static", static_url_path="")
CORS(app)

# Load questions
questions_file_path = os.path.join(os.path.dirname(__file__), "questions.json")
with open(questions_file_path, "r") as f:
    questions = json.load(f)

# Serve API
@app.route("/api/questions")
def get_questions():
    return jsonify(questions)

# Serve index.html
@app.route("/")
def index():
    return send_from_directory("../static", "index.html")

# Serve other static files like script.js
@app.route("/<path:path>")
def static_files(path):
    return send_from_directory("../static", path)
