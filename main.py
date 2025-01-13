import json
from flask import Flask, request, jsonify
from flask_cors import CORS

with open('./resourses/answers_lower.json', 'r', encoding='utf-8') as f:
    answers = json.load(f)

app = Flask(__name__)
CORS(app)

# def ask_chatgpt(question: str, variants: str) -> int:
#     chat_gpt_answer: str = chat.send_message(f"{question}\n{variants}") 
#     chat_gpt_answer = chat_gpt_answer.text.strip()
#     try:
#         chat_gpt_answer = int(chat_gpt_answer)
#         return chat_gpt_answer
#     except ValueError:
#         return -1

@app.route('/solve', methods=['POST'])
def test():
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


app.run(port=5000, debug=True)
