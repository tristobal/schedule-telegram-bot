import os

TOKEN = os.environ.get('TELEGRAM_TOKEN')
URL = os.environ.get('RENDER_URL')
ON_HEROKU = os.environ.get('ON_HEROKU', False)
