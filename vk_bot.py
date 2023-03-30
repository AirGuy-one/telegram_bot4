import os
import random
import vk_api as vk
import redis
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from dotenv import load_dotenv
from get_question_and_answer import get_random_question_and_answer, parse_question_and_answers


def implement_redis_connection():
    return redis.Redis(
        host='redis-18165.c93.us-east-1-3.ec2.cloud.redislabs.com',
        port=18165,
        username='default',
        password='WzTn5YXxs9GBKmTagIumPT6G3WwiiRGS'
    )


NEW_QUESTION, SOLUTION_ATTEMPT, GIVE_UP = range(3)


def start(event, vk_api):
    keyboard = VkKeyboard(one_time=True)

    keyboard.add_button('Новый вопрос', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Сдаться', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button('Мой счёт', color=VkKeyboardColor.SECONDARY)

    vk_api.messages.send(
        user_id=event.user_id,
        message='Привет! Я бот-викторина. Нажми кнопку "Новый вопрос", чтобы начать игру.',
        random_id=random.randint(1, 1000),
        keyboard=keyboard.get_keyboard()
    )


def quiz(event, vk_api):
    r = implement_redis_connection()
    questions, answers = parse_question_and_answers()
    question, answer = get_random_question_and_answer(questions, answers)
    r.set(str(event.user_id), question)
    r.set(str(event.user_id) + 'answer', answer)

    keyboard = VkKeyboard(one_time=True)

    keyboard.add_button('Новый вопрос', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Сдаться', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button('Мой счёт', color=VkKeyboardColor.SECONDARY)

    answer = r.get(str(event.user_id) + 'answer')
    if event.text == 'Новый вопрос':
        vk_api.messages.send(
            user_id=event.user_id,
            message=r.get(str(event.user_id)).decode('utf-8'),
            random_id=random.randint(1, 1000),
            keyboard=keyboard.get_keyboard()
        )
    elif event.text == answer:
        vk_api.messages.send(
            user_id=event.user_id,
            message='Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»',
            random_id=random.randint(1, 1000),
            keyboard=keyboard.get_keyboard()
        )
    elif event.text == 'Сдаться':
        vk_api.messages.send(
            user_id=event.user_id,
            message=f'Правильный ответ: {answer}. Для следующего вопроса нажми «Новый вопрос»',
            random_id=random.randint(1, 1000),
            keyboard=keyboard.get_keyboard()
        )
    else:
        vk_api.messages.send(
            user_id=event.user_id,
            message='Неправильно... Попробуешь ещё раз?',
            random_id=random.randint(1, 1000),
            keyboard=keyboard.get_keyboard()
        )


if __name__ == "__main__":
    load_dotenv()

    vk_session = vk.VkApi(token=os.environ.get('VK_BOT_TOKEN'))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if event.text == '/start':
                start(event, vk_api)
            else:
                quiz(event, vk_api)
