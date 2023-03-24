import os
import telebot

from dotenv import load_dotenv
from main import get_random_question_and_answer


question, answer = get_random_question_and_answer()

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


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    if message.text == 'Новый вопрос':
        bot.reply_to(message, question)
    elif message.text == 'Сдаться':
        bot.reply_to(message, 'You pressed button 2')
    elif message.text == 'Мой счёт':
        bot.reply_to(message, 'You pressed button 3')
    else:
        bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    bot.infinity_polling()
