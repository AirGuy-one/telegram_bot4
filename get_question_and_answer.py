import os
from random import randint
from dotenv import load_dotenv

load_dotenv()


def parse_question_and_answers(path_to_questions):
    with open(path_to_questions, "r", encoding='KOI8-R') as f:
        file_contents = f.read()

    amount = ''
    all_phrases = []
    questions = []
    answers = []
    q, a = 0, 0

    for symbol in file_contents:
        if symbol != '\n':
            amount += symbol
        else:
            all_phrases.append(amount)
            amount = ''

    # Split into questions and answers
    tmp_answer = ''
    tmp_question = ''
    for phrase in all_phrases:
        if q == 1:
            tmp_question += phrase
            q -= 1
            if phrase == '':
                questions.append(tmp_question)
                tmp_question = ''
            else:
                q += 1
        if a == 1:
            tmp_answer += phrase
            a -= 1
            if phrase == '':
                answers.append(tmp_answer)
                tmp_answer = ''
            else:
                a += 1
        if phrase[:6] == 'Вопрос':
            q += 1
        if phrase == 'Ответ:':
            a += 1

    return questions, answers


def get_random_question_and_answer(questions, answers):
    qstn_num = randint(0, len(questions) - 1)
    return questions[qstn_num], answers[qstn_num]
