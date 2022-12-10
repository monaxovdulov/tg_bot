import requests
import pprint
import time
import random

from settings import TOKEN

replics = ["привет", "как дела?", "кто ты?"]
answers = [
    ['привет', 'ЗДАРОВА', 'ХАЙ'],
    ["НОРМ", "ХОРОШО", "КУЛ"],
    ["ты", "я робот, как и ты ", "Павел Дуров"]
]

URL = 'https://api.telegram.org/bot'


def get_updates(offset=0):
    """Returned a list with message
    :param offset:
    :return:
    """
    result = requests.get(f'{URL}{TOKEN}/getUpdates?offset={offset}').json()
    return result['result']


def send_message(text, chat_id):
    requests.get(f"{URL}{TOKEN}/sendMessage?chat_id={chat_id}&text={text}")


pprint.pprint(get_updates())


def run():
    update_id = get_updates()[-1]['update_id']  # Присваиваем ID последнего отправленного сообщения боту
    while True:
        time.sleep(2)
        messages = get_updates(update_id)  # Получаем обновления
        for message in messages:
            # Если в обновлении есть ID больше чем ID последнего сообщения, значит пришло новое сообщение
            if update_id < message['update_id']:
                update_id = message['update_id']  # Присваиваем ID последнего отправленного сообщения боту

                message_user = message['message']['text'].lower()
                if message_user in replics:
                    random_answer = random.choice(answers[replics.index(message_user)])
                    send_message(random_answer, message['message']['chat']['id'])
                print(f"ID пользователя: {message['message']['chat']['id']}, Сообщение: {message['message']['text']}")


run()
