import os
import redis

from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters
from get_question_and_answer import get_random_question_and_answer, parse_question_and_answers

r = redis.Redis(
    host='redis-18165.c93.us-east-1-3.ec2.cloud.redislabs.com',
    port=18165,
    username='default',
    password='WzTn5YXxs9GBKmTagIumPT6G3WwiiRGS'
)

NEW_QUESTION, SOLUTION_ATTEMPT, GIVE_UP = range(3)


async def start(update: Update, context) -> int:
    reply_keyboard = [['Новый вопрос', 'Сдаться'], ['Мой счёт']]
    await update.message.reply_html(
        rf"Привет, я бот для викторин!",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )
    return NEW_QUESTION


async def handle_new_question_request(update: Update, context) -> int:
    questions, answers = parse_question_and_answers()
    question, answer = get_random_question_and_answer(questions, answers)
    # Here we put to database {chat_id}-question pair and {chat_id}chat_id-answer
    r.set(str(update.message.chat_id), question)
    r.set(str(update.message.chat_id) + 'answer', answer)
    await update.message.reply_text(r.get(str(update.message.chat_id)).decode('utf-8'))
    return SOLUTION_ATTEMPT


async def handle_solution_attempt(update: Update, context) -> int:
    answer = r.get(str(update.message.chat_id) + 'answer')
    if update.message.text == answer:
        await update.message.reply_text('Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»')
        return NEW_QUESTION
    elif update.message.text == 'Сдаться':
        await update.message.reply_text(f'Правильный ответ: {answer}. Для следующего вопроса нажми «Новый вопрос»')
        return NEW_QUESTION
    else:
        await update.message.reply_text('Неправильно... Попробуешь ещё раз?')
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
    load_dotenv()

    main()
