import json
import os

import requests
from flask import Flask, request, Response

from scraper.schedule import search_schedule, now
from util.constants import TOKEN, URL

app = Flask(__name__)


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


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        try:
            chat_id, txt = parse_message(msg)
            if txt.lower() == 'buscar':
                send_message(chat_id, f'Ok, voy a buscar la disponibilidad')
                send_message(chat_id, f'{search_schedule()}')
            else:
                send_message(chat_id, f'Tú me dices "{txt}", yo te digo lo mismo en mayúsculas: {txt.upper()}')
        except KeyError as e:
            print(f'{now} Error parsing message from Telegram: {e}')
            print(f'{now} {e}')
        return Response('ok', status=200)
    else:
        return "Nothing to see here"


@app.route('/webhook', methods=['GET'])
def webhook():
    res = requests.get(f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={URL}")
    print(f'{now} {res.text}')
    return Response(res.json()['description'], status=res.status_code)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(port=port, host='0.0.0.0', threaded=True)
