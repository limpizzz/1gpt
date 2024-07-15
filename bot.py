import json
import logging
import telebot
from gpt import post, nez
from info import information
from mytoken import token
from gpt import continuee
bot = telebot.TeleBot(token=token)
users = {}
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="log_file.txt",
    filemode="w",
)
@bot.message_handler(commands=['continue'])
def next_step(message):
    with open('promt.json', 'r') as file:
        data = json.load(file)
        for item in data.values():
            if str(message.chat.id) in item:
                break
            next = continuee(item)
            print(item)
            gpt_response = next.json()['choices'][0]['message']['content']
            bot.send_message(message.chat.id, gpt_response)
            save_promt = item + gpt_response
            with open('promt.json', 'w') as file:
                id1 = message.chat.id
                data = {id1: save_promt}
                json.dump(data, file)


def gpt(message):
    users[message.chat.id]["vvod"] = True
    logging.info("запрос")
    resp = post(message.text, users[message.chat.id]["bot"])
    if resp.status_code == 200 and 'choices' in resp.json():
        if resp.json()['usage']['prompt_tokens'] < 500:
            gpt_response = resp.json()['choices'][0]['message']['content']
            users[message.chat.id]["vvod"] = False

            bot.send_message(message.chat.id, gpt_response)

            with open('promt.json', 'w') as file:
                id1 = message.chat.id
                data = {id1: gpt_response}
                json.dump(data, file)

            logging.info("ответ получен")
            if users[message.chat.id]["debug"]:
                with open("log_file.txt", "rb") as f:
                    bot.send_document(message.chat.id, f)


        else:
            bot.send_message(message.chat.id, "Слишком большое количество токенов, сократи вопрос")
            logging.info("много токенов")
            if users[message.chat.id]["debug"]:
                with open("log_file.txt", "rb") as f:
                    bot.send_document(message.chat.id, f)
            bot.register_next_step_handler(message, gpt)

    else:
        bot.send_message(message.chat.id, resp.json())
        logging.warning("ошибка def gpt")
        if users[message.chat.id]["debug"]:
            with open("log_file.txt", "rb") as f:
                bot.send_document(message.chat.id, f)


def add_user(id):
    if not id in users:
        users[id] = {"debug": False, "bot": "math", "vvod": False}


@bot.message_handler(content_types=['text'])
def vvod(message):
    add_user(message.chat.id)
    if not users[message.chat.id]["vvod"]:
        if message.text == "/start":
            logging.info("start")
            bot.send_message(message.chat.id, information["/start"], reply_markup = nez())
        elif message.text == "/send":
            bot.register_next_step_handler(message, gpt)
            logging.info("/send")
        elif message.text == "/debug":
            if not users[message.chat.id]["debug"]:
                users[message.chat.id]["debug"] = True
                logging.info("debug режим включен")
                bot.send_message(message.chat.id, "вы включили Debug")
                with open("log_file.txt", "rb") as f:
                    bot.send_document(message.chat.id, f)
            elif users[message.chat.id]["debug"]:
                users[message.chat.id]["debug"] = False
                logging.info("debug режим выключен")
                bot.send_message(message.chat.id, "вы выключили Debug")

        else:
            bot.send_message(message.chat.id, "не знаю такой команды")
            logging.info("неизвестная команда")
    else:
        bot.send_message(message.chat.id, "подождите пока бот отправит ответ")
        logging.info("Ожидание ответа")

bot.polling()
