from bs4 import BeautifulSoup
import json

question_block_template = """
<div class="box box-default question" id="question_1">
    <div class="box-header with-border">
        <h3 class="box-title">
            {title}
        </h3>
    </div>
    <div class="box-body checkbo checkbo-ready">
        
        {variants_block}

    </div>
    </div>
"""
variant_block_template = """
<p>
    <label class="cb-radio" for="test_question_{question_num}_{variant_num}">
        <span class="cb-inner">
            <i>
                <input
                    type="radio"
                    onchange="setAnswer(this,548953,{variant_num})"
                    value="{variant_num}"
                    name="test_question_{question_num}"
                    id="test_question_{question_num}_{variant_num}"
                />
            </i>
        </span>
        <span class="qv"> {variant_text} </span>
    </label>
</p>
"""

with open("./resourses/alghoritms_hemis_test_full.json", 'r', encoding='utf-8') as f:
    questions_answers_full = json.load(f)

old_html_file_path = "./sample_exam_file.html"
with open(old_html_file_path, 'r', encoding='utf-8') as f:
    old_html_file_text = f.read()
soup = BeautifulSoup(old_html_file_text, 'lxml')
questions_parent = soup.find('div', {"class": "question"} ).parent

for question_html_block in soup.find_all("div", {"class": "question"}):
    question_html_block.decompose()


questions = list(questions_answers_full.keys())[:50]
variants = list(questions_answers_full.values())[:50]

for question_num in range(1, len(questions) + 1):
    question = questions[question_num - 1]
    q_variants = variants[question_num - 1]
    v_block = ""
    for variant_num in range(len(q_variants)):
        v_block+=variant_block_template.format(question_num=question_num, variant_num=variant_num, variant_text=q_variants[variant_num])
    question_block = question_block_template.format(title=f"{question_num}. {question}", variants_block=v_block)
    
    questions_parent.append(BeautifulSoup(question_block, "lxml"))

with open("index.html", "w", encoding="utf-8") as file:
    file.write(soup.prettify())
    
