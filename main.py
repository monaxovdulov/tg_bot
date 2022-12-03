import requests
import pprint
from settings import TOKEN

URL = 'https://api.telegram.org/bot'


METHOD_getUpdates = '/getUpdates'

METHOD_send_message = '/sendMessage'

METHOD_sendPhoto = '/sendPhoto'

print(URL+TOKEN+METHOD_getUpdates)
updates = requests.get(URL+TOKEN+METHOD_getUpdates).json()
pprint.pprint(updates)

if not updates['result']:
    print("У БОТА НЕТ НОВЫХ СООБЩЕНИЙ")
else:
    chat_id = updates["result"][0]["message"]["chat"]["id"]
    print(chat_id)
    user_choice = input("Что хотите отправить боту\n1 - текстовое сообщение\n2 - картинку\n|$~>")

    if user_choice == '1':
        text = input("Введите что хотите отправить через бота пользователю")
        requests.get(URL+TOKEN+METHOD_send_message+f"?chat_id={chat_id}&text={text}")
    elif user_choice == '2':
        link_to_picture = input("Введите ссылку на картинку:")
        requests.get(URL+TOKEN+METHOD_sendPhoto+f"?chat_id={chat_id}&caption=kek&photo={link_to_picture}")
