import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from ai import chat
import unidecode

with open('./resourses/alghoritms_hemis_test.html.json', 'r', encoding='utf-8') as f:
    answers = json.load(f)

with open("./resourses/alghoritms_hemis_test.html_latin.json", "r", encoding="utf-8") as f:
    answers_latin = json.load(f)

app = Flask(__name__)
CORS(app)


@app.route('/solve', methods=['POST'])
def solve():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    if not data.get("question"):
        return jsonify({"error": "No question provided"}), 400
    if not data.get("variants"):
        return jsonify({"error": "No variants provided"}), 400
    
    question: str = data["question"].lower()
    variants: dict[str, str] = data["variants"]
    # like {"0": "Answer1", "1": "Answer2", "2": "Answer3"}

    if not answers.get(question):
        # answer = ask_chatgpt(question, "\n".join(variants.values()))
        # if answer == -1:
        return jsonify({"error": "No answer found"}), 404
        # return jsonify({"answer": str(answer)})
    
    answer = answers[question]
    # try to find this answer in variants
    try:
        answer = list(variants.keys())[list(variants.values()).index(answer)]
    except ValueError:
        # chat_gpt_answer = ask_chatgpt(question, "\n".join(variants.values()))
        # if chat_gpt_answer == -1:
        return jsonify({"error": "Answer not found"}), 404
        # return jsonify({"answer": chat_gpt_answer})
        # return jsonify({"

    print("Solved: ", question, "Answer: ", answer)
    # return key of variant
    return jsonify({"answer": answer})

@app.route("/ai_solve", methods=["POST"])
def ai_solve():
    # temp_answer = {'question_1': '0', 'question_2': '2', 'question_3': '1', 'question_4': '3', 'question_5': '3', 'question_6': '0', 'question_7': '3', 'question_8': '2', 'question_9': '2', 'question_10': '0', 'question_11': '0', 'question_12': '3', 'question_13': '3', 'question_14': '1', 'question_15': '3', 'question_16': '2', 'question_17': '0', 'question_18': '3', 'question_19': '0', 'question_20': '3'}
    # return jsonify(temp_answer)
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    answers = chat.send_message(str(data)).text
    answers = str(answers.replace("```json", " ").replace("```", " "))
    json_answers = json.loads(answers)
    print(json_answers)
    return jsonify(json_answers)

@app.route("/solve_new_method", methods=["POST"])
def solve_new_method():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    print(data)
    return jsonify({"answer": "0"})


app.run(port=5000, debug=True)
