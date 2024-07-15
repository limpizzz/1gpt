import requests
from telebot import types
from telebot.types import ReplyKeyboardMarkup

system_content = "ты дружелюбный бот помощник по математике"
assistant = 'продолжи свой ответ'

def post(text, bot):
    resp = requests.post(
        'http://158.160.135.104:1234/v1/chat/completions',
        headers={"Content-Type": "application/json"},
        json={
            "messages": [
                {"role": "user", "content": text},
                {"role": "system", "content": f'{system_content}'}
            ],
            "temperature": 0.7,
            "max_tokens": 50,
            "stream": False
        }
    )
    return resp
def continuee(text):
    resp = requests.post(
        ' http://158.160.135.104:1234/v1/chat/completions',
        headers={"Content-Type": "application/json"},
        json={
            "messages": [
                {"role": "system", "content": f'{system_content}'},
                {"role": "assistant", "content": f'{assistant}{text}'}

            ],
            "temperature": 0.7,
            "max_tokens": 50,
            "stream": False
        }
    )
    return resp

def nez():
    keyboard = ReplyKeyboardMarkup()
    btn2 = types.KeyboardButton("/continue")
    keyboard.add(btn2)
    return keyboard


