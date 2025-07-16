from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv
import random
import json


load_dotenv()
with open("fallback_questions.json", "r") as f:
    fallback_questions = json.load(f)

app = Flask(__name__)
CORS(app, resources={r"/generate": {"origins": "http://localhost:8000"}})

openai.api_key = os.getenv("OPENAI_API_KEY")



@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    position = data.get("position", "1st Base")

    prompt = f"""You're a coach helping Little League players understand baseball. Create a game situation specifically for a {position}. It should include:
- One scenario
- Three possible answers
- One correct answer

Format your response like this:
Question: [your question here]
A) [option A]
B) [option B]
C) [option C]
Answer: [correct option letter]
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300
        )

        ai_text = response["choices"][0]["message"]["content"]
        lines = ai_text.split("\n")
        question = lines[0].replace("Question: ", "")
        options = [line[3:] for line in lines[1:4]]
        answer_letter = lines[4].split(": ")[1].strip()
        answer_index = {"A": 0, "B": 1, "C": 2}[answer_letter]

        return jsonify({
            "question": question,
            "options": options,
            "answer": options[answer_index]
        })

    except Exception as e:
        print(f"⚠️ OpenAI Error: {e}")
        fallback = fallback_questions.get(position, fallback_questions["1st Base"])
        fallback_play = random.choice(fallback)
        return jsonify(fallback_play), 200




if __name__ == "__main__":
    app.run(debug=True)
