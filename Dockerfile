FROM python:3.8-slim-buster

WORKDIR /app

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -yqq gnupg2 wget unzip curl

RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -yqq ./google-chrome-stable_current_amd64.deb

RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# set display port to avoid crash
ENV DISPLAY=:99

RUN pip install --upgrade pip

COPY app.py /app/app.py
COPY scraper/ /app/scraper/
COPY util/ /app/util/
COPY telegram/ /app/telegram/
COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 8080

CMD python app.py
#CMD gunicorn app:app

