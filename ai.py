import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
with open("./resourses/alghoritms_hemis_test.html.json", "r", encoding="utf-8") as f:
    answers = f.read()
system_instruction = "Ты студент решаюший тест, тебе будет отправлено json файл, с вопросами и вариантами ответов. Твоя задача выбрать правильный вариант ответа и отправить его. Ты должен решить и вернуть ответ в виде json объекта. Например {\"question_1\": \"0\", \"question_2\": \"1\"} и так далее. Только так и никак иначе. А еще тебе бует отправлен некоторые вопросы с ответами, можешь искать ответы там а если нет то решай сам, но чтоб возвращал только json!!!!"
model = genai.GenerativeModel(
    "gemini-1.5-pro",
    system_instruction=system_instruction,
)

chat = model.start_chat(
    history=[
        {"role": "user", "parts": f"{answers}"},
    ]
)

# question = "Что такое экстронет?"
# answers = [
#     "0. Личная почтовая система для руководства",
#     "1. Внутренний портал компании, доступный только сотрудникам.",
#     "2. Корпоративная сеть, использующая для соединения метасеть Интернет",
#     "3. Специальный кабель для подключения серверов"
# ]

# response = chat.send_message(f"{question}\n{"\n".join(answers)}")
# print(response.text)