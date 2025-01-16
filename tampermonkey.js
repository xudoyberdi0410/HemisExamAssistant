// ==UserScript==
// @name         Hemis Test Assistant
// @namespace    http://tampermonkey.net/
// @version      2025-01-12
// @description  try to take over the world!
// @author       You
// @match        https://student.fbtuit.uz/*
// @match        http://127.0.0.1:5500/*
// @match        https://7fjt674h-5500.euw.devtunnels.ms/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=0.1
// @grant        none
// ==/UserScript==
(function() {
    'use strict';
    // Your code here...
    const addon = `
<div>
    <div class="khudoberdi-modal">
        <div class="khudoberdi-right kh-h">
            <button id="auto-solve-btn">Solve</button>
            <button id="ai-solve-btn">AI Solve</button>
            <!-- <iframe src="https://drive.google.com/file/d/1wComPezg7huYW9-oOgeA_SIqvij2ywKE/preview" allow="autoplay" height="300px"></iframe> -->
            <iframe src="https://raw.githubusercontent.com/xudoyberdi0410/HemisExamAssistant/refs/heads/main/templates/alghoritms_hemis_test.html"  allow="autoplay" height="300px"></iframe>
        </div>
    </div>
    <style>
        .kh-h {
            opacity: 0;
        }
        .kh-h:hover {
            opacity: 1;
        }

        .khudoberdi-right{
            display: flex;
            flex-direction: column;
            width: 500px;
            height: 300px;
            bottom: 0;
            right: 0;
            position: fixed;
        }
        #auto-solve-btn{
            padding: 4px;
            color: #232323;
            background-color: aquamarine;
            cursor: pointer;
            border: 1px solid #232323;
            border-radius: 3px;
        }
    </style>
</div>
`
    const parser = new DOMParser()
    const doc = parser.parseFromString(addon, "text/html")
    document.body.appendChild(doc.body)

    const right_el = document.querySelector('.khudoberdi-right')
    const modal = document.querySelector('.khudoberdi-modal')

    let hide_all = true
    let position = 'right'

    document.addEventListener('keydown', function (event) {
        if (event.key === '*') {
            if (position === 'right') {
                right_el.style.right = ''
                right_el.style.left = '0'
                position = 'left'
            } else {
                right_el.style.left = ''
                right_el.style.right = '0'
                position = 'right'
            }
        }
        // resize right element
        if (event.key === '-') {
            right_el.style.width = right_el.offsetWidth - 10 + 'px'
            right_el.style.height = right_el.offsetHeight - 10 + 'px'
        }
        if (event.key === '+') {
            right_el.style.width = right_el.offsetWidth + 10 + 'px'
            right_el.style.height = right_el.offsetHeight + 10 + 'px'
        }

        // hide all elements
        if (event.key === 'h') {
            const correct_answers = this.querySelectorAll("*[answer=true]")
            if (hide_all) {
                modal.style.display = 'none'
                correct_answers.forEach(correct_answer => {
                    correct_answer.style.borderBottom = ''
                })
            } else {
                modal.style.display = 'block'
                correct_answers.forEach(correct_answer => {
                    correct_answer.style.borderBottom = '1px solid rgba(0, 0, 0, 0.1)'
                })
            }
            hide_all = !hide_all
        }
    })

    document.getElementById('auto-solve-btn').onclick = solve_all
    document.getElementById('ai-solve-btn').onclick = ai_solve_btn_onclick

})();
function get_questions_and_variants(){
    let questions_blocks = document.querySelectorAll('.question')
    let questions = {}
    questions_blocks.forEach(block => {
        let question = block.querySelector('h3').innerText
        question = question.trim().replace(/^\d+\.\s*/, '')
        let question_id = block.id

        let variants = {}
        let variants_tag = block.querySelectorAll('p')
        for (let i = 0; i < variants_tag.length; i++) {
            variants[variants_tag[i].querySelector('input').value] = variants_tag[i].querySelector(".qv").innerText.toLocaleLowerCase()
        }
        questions[question_id] = {
            'question': question,
            'variants': variants
        }
    })
    return questions
}
async function solve_all() {
    const backend_url = 'http://16.171.237.185/solve_new_method';
    const questions = get_questions_and_variants();
    console.log(questions);
    let i = 0
    for (const [key, value] of Object.entries(questions)) {
        let question_id = key;
        let question = value['question'];
        let variants = value['variants'];

        try {
            const response = await fetch(backend_url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    question: question,
                    variants: variants,
                }),
            });

            let data = await response.json();
            data = data.answer

            let question_block = document.querySelector(`#${question_id}`)
            console.log(question_block);
            // add border bottom to correct answer
            let correct_answer = question_block.querySelector(`input[type="radio"][value="${data}"]`).parentElement.parentElement.parentElement


            correct_answer.setAttribute('answer', 'true')
            correct_answer.style.borderBottom = '1px solid rgba(0, 0, 0, 0.1)'
        } catch (error) {
            console.error(`Error processing question ${question_id}:`, error);
        }
    }
}
async function ai_solve_btn_onclick(){
    const backend_url = 'http://16.171.237.185/solve_new_method';
    const questions = get_questions_and_variants();

    let answers = await fetch(backend_url, {
        'headers': {
            'Content-Type': 'application/json'
        },
        'method': 'POST',
        'body': JSON.stringify(questions)
    })
    answers = await answers.json()
    for (const [key, value] of Object.entries(answers)) {
        let question_id = key
        let answer_value = value
        console.log(value)
        let question_block = document.querySelector(`#${question_id}`)
        let correct_answer = question_block.querySelector(`input[type="radio"][value="${answer_value}"]`).parentElement.parentElement.parentElement
        correct_answer.setAttribute('answer', 'true')
        correct_answer.style.borderBottom = '1px solid rgba(0, 0, 0, 0.1)'
    }

}