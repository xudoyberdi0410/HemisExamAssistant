const background_url = 'https://khudoberdi.uz/';
const addon = `
<div>
    <div class="khudoberdi-modal">
        <div class="khudoberdi-right kh-h">
            <button id="auto-solve-btn">Solve</button>
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
        .correct-answer {
    background-color: transparent; /* По умолчанию ничем не выделяется */
    position: relative;
}

.correct-answer::after {
    content: ""; /* Добавляем элемент */
    position: absolute;
    width: 5px;
    height: 5px;
    border-radius: 50%; /* Маленький кружок */
    background-color: rgba(0, 0, 0, 0.1); /* Едва заметный цвет */
    bottom: 50%;
    right: -10px;
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
                    // correct_answer.style.borderBottom = '1px solid rgba(0, 0, 0, 0.1)'
                    correct_answer.style.borderRadius = ''
                })
            }
            hide_all = !hide_all
        }
    })

    document.getElementById('auto-solve-btn').onclick = ai_solve_btn_onclick

function get_questions_and_variants(){
    let questions_blocks = document.querySelectorAll('.question')
    let questions = {}
    questions_blocks.forEach(block => {
        let question = block.querySelector('h3').innerText
        question = question.trim().replace(/^\d+\.\s*/, '')
        question_id = block.id
        
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

async function ai_solve_btn_onclick(){
    const backend_url = `${background_url}ai_solve`;
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
        console.log(question_id, answer_value)
        let question_block = document.querySelector(`#${question_id}`)
        let correct_answer = question_block.querySelector(`input[type="radio"][value="${answer_value}"]`).parentElement.parentElement.parentElement
        correct_answer.setAttribute('answer', 'true')
        // correct_answer.style.borderBottom = '1px solid rgba(0, 0, 0, 0.1)'
        correct_answer.style.borderRadius = '10px'
    }
}