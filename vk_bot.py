import os
import random

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from dotenv import load_dotenv

load_dotenv()


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


def echo(event, vk_api):
    keyboard = VkKeyboard(one_time=True)

    keyboard.add_button('Новый вопрос', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Сдаться', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button('Мой счёт', color=VkKeyboardColor.SECONDARY)

    vk_api.messages.send(
        user_id=event.user_id,
        message=event.text,
        random_id=random.randint(1, 1000),
        keyboard=keyboard.get_keyboard()
    )


if __name__ == "__main__":
    vk_session = vk.VkApi(token=os.environ.get('VK_BOT_TOKEN'))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if event.text == '/start':
                start(event, vk_api)
            else:
                echo(event, vk_api)
