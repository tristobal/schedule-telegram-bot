# Scrapper Telegram Bot
## Work in progress

Flask service to search in a webpage when a specific doctor has open agenda.


https://render.com/docs/configure-environment-variables

### Run locally
#### Install requirements and Chromedrive
```bash
# Dependencies and virtual environment
$ python -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt

# Chromedriver
$ wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
$ unzip /tmp/chromedriver.zip chromedriver -d .
```

#### Run
```bash
(venv) $ python app.py
```