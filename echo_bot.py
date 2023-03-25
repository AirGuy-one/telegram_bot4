import os

from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters
from get_question_and_answer import get_random_question_and_answer
from db_connection import set_up_db_connection, set_question, get_question

r = set_up_db_connection()

load_dotenv()

answer = ''

NEW_QUESTION, SOLUTION_ATTEMPT, GIVE_UP = range(3)


async def start(update: Update, context) -> int:
    reply_keyboard = [['Новый вопрос', 'Сдаться'], ['Мой счёт']]
    await update.message.reply_html(
        rf"Привет, я бот для викторин!",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )
    return NEW_QUESTION


async def help_command(update: Update, context) -> None:
    await update.message.reply_text("Help!")


async def handle_new_question_request(update: Update, context) -> int:
    global answer
    question, answer = get_random_question_and_answer()
    set_question(r, update.message.chat_id, question)
    await update.message.reply_text(get_question(r, update.message.chat_id))
    return SOLUTION_ATTEMPT


async def handle_solution_attempt(update: Update, context) -> int:
    global answer
    if update.message.text == answer:
        await update.message.reply_text('Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»')
        return NEW_QUESTION
    elif update.message.text == 'Сдаться':
        await update.message.reply_text(f'Правильный ответ: {answer}. Для следующего вопроса нажми «Новый вопрос»')
        return NEW_QUESTION
    else:
        await update.message.reply_text(f'Неправильно... Попробуешь ещё раз?')
        return SOLUTION_ATTEMPT


def main() -> None:
    application = Application.builder().token(os.environ.get('TG_BOT_TOKEN')).build()

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NEW_QUESTION: [
                MessageHandler(filters=filters.Regex('^Новый вопрос$'), callback=handle_new_question_request)],
            SOLUTION_ATTEMPT: [
                MessageHandler(filters=filters.Regex('^(?!Сдаться).*$'), callback=handle_solution_attempt)],
        },
        fallbacks=[MessageHandler(filters=filters.Regex('^Сдаться$'), callback=handle_solution_attempt)],
    )

    application.add_handler(conversation_handler)
    application.add_handler(CommandHandler("help", help_command))
    application.run_polling()


if __name__ == "__main__":
    main()
