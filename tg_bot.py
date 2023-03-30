import os
import redis
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters
from get_question_and_answer import get_random_question_and_answer, parse_question_and_answers


def implement_redis_connection():
    return redis.Redis(
        host='redis-18165.c93.us-east-1-3.ec2.cloud.redislabs.com',
        port=18165,
        username='default',
        password='WzTn5YXxs9GBKmTagIumPT6G3WwiiRGS'
    )


async def start(update: Update, context) -> int:
    reply_keyboard = [['Новый вопрос', 'Сдаться'], ['Мой счёт']]
    await update.message.reply_html(
        rf"Привет, я бот для викторин!",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )
    return 0


async def handle_new_question_request(update: Update, context) -> int:
    r = implement_redis_connection()
    questions, answers = parse_question_and_answers()
    question, answer = get_random_question_and_answer(questions, answers)
    # Here we put to database {chat_id}-question pair and {chat_id}chat_id-answer
    r.set(str(update.message.chat_id), question)
    r.set(str(update.message.chat_id) + 'answer', answer)
    await update.message.reply_text(r.get(str(update.message.chat_id)).decode('utf-8'))
    return 1


async def handle_solution_attempt(update: Update, context) -> int:
    r = implement_redis_connection()
    answer = r.get(str(update.message.chat_id) + 'answer')
    if update.message.text == answer:
        await update.message.reply_text('Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»')
        return 0
    elif update.message.text == 'Сдаться':
        await update.message.reply_text(f'Правильный ответ: {answer}. Для следующего вопроса нажми «Новый вопрос»')
        return 0
    else:
        await update.message.reply_text('Неправильно... Попробуешь ещё раз?')
        return 1


def main() -> None:
    application = Application.builder().token(os.environ.get('TG_BOT_TOKEN')).build()

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            0: [
                MessageHandler(filters=filters.Regex('^Новый вопрос$'), callback=handle_new_question_request)],
            1: [
                MessageHandler(filters=filters.Regex('^(?!Сдаться).*$'), callback=handle_solution_attempt)],
        },
        fallbacks=[MessageHandler(filters=filters.Regex('^Сдаться$'), callback=handle_solution_attempt)],
    )

    application.add_handler(conversation_handler)
    application.run_polling()


if __name__ == "__main__":
    load_dotenv()

    main()
