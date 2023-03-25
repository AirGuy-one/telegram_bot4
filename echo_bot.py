import os

from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from get_question_and_answer import get_random_question_and_answer
from db_connection import set_up_db_connection, set_question, get_question

r = set_up_db_connection()

load_dotenv()

answer = ''
counter = 0


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_keyboard = [['Новый вопрос', 'Сдаться'], ['Мой счёт']]
    await update.message.reply_html(
        rf"Привет, я бот для викторин!",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Help!")


async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global answer, counter

    if update.message.text == 'Новый вопрос':
        question, answer = get_random_question_and_answer()
        set_question(r, update.message.chat_id, question)
        counter += 1
        await update.message.reply_text(get_question(r, update.message.chat_id))
    elif update.message.text == 'Сдаться':
        await update.message.reply_text("Do not give up")
    elif update.message.text == 'Мой счёт':
        await update.message.reply_text("This is your bill")
    elif update.message.text == answer:
        counter -= 1
        await update.message.reply_text('Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»')
    else:
        if counter == 0:
            reply_keyboard = [['Новый вопрос', 'Сдаться'], ['Мой счёт']]
            counter = 0
            await update.message.reply_text(
                'Привет, я бот для викторин!',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
            )
        else:
            await update.message.reply_text('Неправильно... Попробуешь ещё раз?')


def main() -> None:
    application = Application.builder().token(os.environ.get('TG_BOT_TOKEN')).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, quiz))
    application.run_polling()


if __name__ == "__main__":
    main()
