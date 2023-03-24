import os
import telebot

from dotenv import load_dotenv
from main import get_random_question_and_answer
from db_connection import set_up_db_connection, set_question, get_question

r = set_up_db_connection()

load_dotenv()


BOT_TOKEN = os.environ.get('TG_BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

custom_keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
btn1 = telebot.types.KeyboardButton('Новый вопрос')
btn2 = telebot.types.KeyboardButton('Сдаться')
btn3 = telebot.types.KeyboardButton('Мой счёт')
custom_keyboard.add(btn1, btn2, btn3)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the club, buddy!", reply_markup=custom_keyboard)


answer = None


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    global answer

    if message.text == 'Новый вопрос':
        question, answer = get_random_question_and_answer()
        set_question(r, message.chat.id, question)
        bot.reply_to(
            message,
            get_question(r, message.chat.id)
        )
    elif message.text == 'Сдаться':
        bot.reply_to(message, 'You pressed button 2')
    elif message.text == 'Мой счёт':
        bot.reply_to(message, 'You pressed button 3')
    elif message.text == answer:
        bot.reply_to(message, 'Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»')
    else:
        bot.send_message(message.chat.id, 'Неправильно… Попробуешь ещё раз?')


if __name__ == '__main__':
    bot.infinity_polling()
