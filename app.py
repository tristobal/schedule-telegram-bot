from flask import Flask, request, Response
from telebot.credentials import TOKEN, URL
from scraper.schedule import search_schedule, now
import json
import requests
import schedule

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
        chat_id, txt = parse_message(msg)
        if txt.lower() == 'buscar':
            send_message(chat_id, f'Ok, voy a buscar la disponibilidad')
            send_message(chat_id, f'{search_schedule()}')
        elif txt == 'programar':
            tel_send_poll(chat_id)
        else:
            send_message(chat_id, f'Tú me dices "{txt}", yo te digo lo mismo en mayúsculas: {txt.upper()}')
        return Response('ok', status=200)
    else:
        return "Nothing to see here"


def job():
    print(f"{now()} Hola mundo")


def tel_send_poll(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendPoll'
    payload = {
        'chat_id': chat_id,
        "question": "¿En qué centro asistencial quiere agendar?",
        "options": json.dumps(["Integramédica", "Redsalud", "Avansalud", "Hospital de Quillota"]),
        "is_anonymous": False,
        "type": "quiz",
        "correct_option_id": 2
    }

    r = requests.post(url, json=payload)

    return r

if __name__ == '__main__':
    try:
        response = requests.get(f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={URL}")
        if response.status_code == 200:
            print(f"response: {response.json()}")
            schedule.every(1).minutes.do(job)
            app.run(debug=True)
        else:
            raise RuntimeError(f"{response.status_code} ")
    except (requests.exceptions.RequestException, RuntimeError) as e:
        raise SystemExit(e)
