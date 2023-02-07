import json

import requests

from util.constants import TOKEN, URL

WEBHOOK_URL = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={URL}"


def parse_message(message):
    print(json.dumps(message, indent=2, sort_keys=True))
    chat_id = message['message']['chat']['id']
    txt = message['message']['text']
    print(f"chat_id: {chat_id}")
    print(f"txt: {txt}")
    return chat_id, txt


def send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    req = requests.post(url, json=payload)
    return req

