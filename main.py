import json
from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
from ai import chat
import unidecode
from typing import Dict, Union
from tenacity import retry, stop_after_attempt, stop_after_delay
import zipfile

with open('./resourses/answers.json', 'r', encoding='utf-8') as f:
    answers = json.load(f)

with open("./resourses/answers_latin.json", "r", encoding="utf-8") as f:
    answers_latin: dict[str, str] = json.load(f)

app = Flask(__name__)
CORS(app)

@retry(stop_after_attempt(3), stop_after_delay(5))
def ask_ai(unsolved_questions):
    try:
        answers_ai = chat.send_message(str(unsolved_questions)).text
        
        answers_ai_corrected = str(answers_ai.replace("```json", " ").replace("```", " "))
        json_answers = json.loads(answers_ai_corrected)
        return json_answers
    except Exception:
        print("cant get correct answer from gemeni, answer: ", answers_ai)
        return {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/ai_solve", methods=["POST"])
def solve_new_method():
    data: Dict[str, Union[str, Dict[str, Dict[str, str]]]] = request.json
    print(data)
    if not data:
        return jsonify({"error": "No data provided"}), 400
    unsolved_questions = {}
    answers = {}
    for question_id, question_and_variants in data.items():
        latin_question = unidecode.unidecode(question_and_variants["question"].lower())

        if answers_latin.get(latin_question):
            for key, value in question_and_variants["variants"].items():
                if unidecode.unidecode(value.lower()) == answers_latin[latin_question]:
                    print("Found: ", value)
                    answers[question_id] = key
        else:
            print("Not found", latin_question)
            unsolved_questions[question_id] = question_and_variants
    print(len(unsolved_questions), len(answers))
    if len(unsolved_questions) != 0:
        try:
            # answers_ai = chat.send_message(str(unsolved_questions)).text
            # print(answers_ai)
            
            # answers_ai = str(answers_ai.replace("```json", " ").replace("```", " "))
            # json_answers = json.loads(answers_ai)
            answers.update(ask_ai(unsolved_questions))
            ...
        except Exception:
            print("Can't")
    return jsonify(answers)

@app.route('/x_variants', methods=['GET'])
def x_variants():
    return render_template('pc.html')

@app.route("/extension", methods=["GET"])
def extension():
    return send_file("./ext.zip", as_attachment=True)

@app.route("/install", methods=["GET"])
def install():
    return send_file("./install.ps1", as_attachment=True)

app.run(port=5000, debug=True)
