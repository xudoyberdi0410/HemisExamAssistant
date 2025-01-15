import tiktoken
enc = tiktoken.get_encoding("o200k_base")

with open("./resourses/alghoritms_hemis_test.html.json", "r", encoding="utf-8") as f:
    answers = f.read()



assert enc.decode(enc.encode(answers)) == answers

# To get the tokeniser corresponding to a specific model in the OpenAI API:
enc = tiktoken.encoding_for_model("gpt-4o")
