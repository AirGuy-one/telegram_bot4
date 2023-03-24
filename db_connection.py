import redis


def set_up_db_connection():
    return redis.Redis(
        host='redis-18165.c93.us-east-1-3.ec2.cloud.redislabs.com',
        port=18165,
        username='default',
        password='WzTn5YXxs9GBKmTagIumPT6G3WwiiRGS'
    )


def set_question(r, chat_id, question):
    r.set(str(chat_id), question)


def get_question(r, chat_id):
    return r.get(str(chat_id))
