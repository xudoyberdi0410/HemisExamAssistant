import requests
import random
import json
from tenacity import retry, stop_after_attempt, stop_after_delay
from ai import chat

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

with open("./resourses/alghoritms_hemis_test_full.json", 'r', encoding='utf-8') as f:
    answers_database = json.load(f)

random_questions = random.sample(list(answers_database.items()), 50)

# Формирование нового словаря с перемешанными вариантами
result = {}
correct_answers_mapping = {}  # Для отслеживания правильных вариантов

for idx, (question, variants) in enumerate(random_questions, 1):
    # Перемешиваем варианты
    shuffled_variants = random.sample(variants, len(variants))
    
    # Сохраняем индекс правильного ответа после перемешивания
    correct_answer_idx = variants.index(variants[0])  # Правильный вариант из исходного набора
    correct_shuffled_idx = shuffled_variants.index(variants[0])  # Индекс правильного ответа в перемешанном наборе
    
    correct_answers_mapping[f'question_{idx}'] = correct_shuffled_idx  # Сохраняем индекс правильного ответа
    
    result[f'question_{idx}'] = {
        'question': question,
        'variants': {str(i): variant for i, variant in enumerate(shuffled_variants)}
    }

server_response = ask_ai(result)

correct_answers = 0
incorrect_answers = []  # Список для хранения информации о неправильных ответах

for question_id, selected_answer in server_response.items():
    # Получаем правильный индекс ответа после перемешивания
    correct_shuffled_idx = correct_answers_mapping.get(question_id)
    
    # Получаем информацию о вопросе и вариантах
    question_text = result.get(question_id, {}).get('question', 'Unknown question')
    selected_variant = result.get(question_id, {}).get('variants', {}).get(selected_answer, 'Unknown answer')
    
    # Проверяем, совпадает ли выбранный ответ с правильным
    if int(selected_answer) == correct_shuffled_idx:
        correct_answers += 1
        print(f"Вопрос: {question_text}\nПравильный ответ: {selected_variant}\nОтветил правильно\n")
    else:
        print(result[question_id])
        print(f"Вопрос: {question_text}\nОтвет: {selected_variant}\nОтветил неправильно\n")

# Выводим итоговый результат
total_questions = len(server_response)
print(f"Правильных ответов: {correct_answers} из {total_questions}")
