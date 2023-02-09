import os

import requests
from flask import Flask, request, Response

from scraper.schedule import search_dermatologist_schedule, search_rheumatologist_schedule, now
from telegram.handler import send_message, parse_message, WEBHOOK_URL

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        try:
            chat_id, txt = parse_message(msg)
            if txt.lower() == 'buscar':
                send_message(chat_id, f'Ok, voy a buscar la disponibilidad')
                send_message(chat_id, f'{search_dermatologist_schedule()}')
            elif txt.lower() == 'reuma':
                send_message(chat_id, f'Ok, voy a buscar la disponibilidad de algún reumatólogo')
                send_message(chat_id, f'{search_rheumatologist_schedule()}')
            else:
                msg = "Para buscar la agenda de la dermatóloga, escribe \"buscar\".\n" \
                      "Para buscar cualquier reumatólogo, escribe \"reuma\"."
                send_message(chat_id, msg)
        except KeyError as e:
            print(f'{now} Error parsing message from Telegram: {e}')
            print(f'{now} {e}')
        return Response('ok', status=200)
    else:
        return "Nothing to see here"


@app.route('/scrap', methods=['GET'])
def web_scraper():
    print(f'${now()} web_scraper')
    try:
        response = search_dermatologist_schedule()
        print(f'${now()} {response}')
    except Exception as e:
        response = e
    return Response(response, status=200)


@app.route('/scrap2', methods=['GET'])
def web_scraper2():
    print(f'${now()} web_scraper2')
    try:
        response = search_rheumatologist_schedule()
        print(f'${now()} {response}')
    except Exception as e:
        response = e
    return Response(response, status=200)


@app.route('/webhook', methods=['GET'])
def webhook():
    res = requests.get(WEBHOOK_URL)
    print(f'{now} {res.text}')
    return Response(res.json()['description'], status=res.status_code)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(port=port, host='0.0.0.0', threaded=True)
