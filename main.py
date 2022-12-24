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

key_word_for_quiz = ["играть", "викторина", "game", 'игра']

is_program_run = True

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


def start_quiz(chat_id, upd_id):
    send_message("викторина игра ураа", chat_id)
    questions = requests.get("https://engine.lifeis.porn/api/millionaire.php/?qType=1&count=3").json()
    questions = questions['data']

    for q in questions:
        send_message(q['question'].replace("\u2063", ""), chat_id)
        correct_answer = q['answers'][0]
        option_answer = q['answers']

        random_options_answer = []
        for option in range(len(option_answer)):
            random_option = random.choice(option_answer)
            random_index = option_answer.index(random_option)
            option_answer.pop(random_index)
            random_options_answer.append(random_option)

        send_message("варианты ответа" + '\n'.join(random_options_answer), chat_id)
        input("Ждём ответа на вопрос")
        time.sleep(2)
        messages = get_updates(upd_id)  # Получаем обновления
        for message in messages:
            # Если в обновлении есть ID больше чем ID последнего сообщения, значит пришло новое сообщение
            if upd_id < message['update_id']:
                upd_id = message['update_id']
                message_user = message['message']['text']

                if message_user == correct_answer:
                    send_message("Верно", chat_id)
                else:
                    send_message(" Не Верно", chat_id)

    pprint.pprint(questions)


pprint.pprint(get_updates())


def run():
    if not get_updates():
        return 'empty_list'

    update_id = get_updates()[-1]['update_id']  # Присваиваем ID последнего отправленного сообщения боту
    while True:
        time.sleep(2)
        messages = get_updates(update_id)  # Получаем обновления
        for message in messages:
            # Если в обновлении есть ID больше чем ID последнего сообщения, значит пришло новое сообщение
            if update_id < message['update_id']:
                update_id = message['update_id']  # Присваиваем ID последнего отправленного сообщения боту

                chat_id_current_message = message['message']['chat']['id']
                message_user = message['message']['text'].lower()
                if message_user in replics:
                    random_answer = random.choice(answers[replics.index(message_user)])
                    send_message(random_answer, chat_id_current_message)
                else:
                    for key_word in key_word_for_quiz:
                        if key_word in message_user:
                            start_quiz(chat_id_current_message, update_id)
                            break
                    else:
                        send_message("Я вас понял, но сказать мне нечего", chat_id_current_message)
                print(f"ID пользователя: {message['message']['chat']['id']}, Сообщение: {message['message']['text']}")


program_result = run()
while is_program_run:
    if program_result == 'empty_list':
        print("У бота нет новых сообщений попробуйте написать ему что нибудь,\n а после нажать Enter в консоли")
        input()
        program_result = run()
    else:
        program_result = run()

