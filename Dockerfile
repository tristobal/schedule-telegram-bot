FROM python:3.8-slim-buster

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


WORKDIR /app

COPY app.py /app/app.py
COPY scraper/schedule.py /app/scraper/schedule.py
COPY util/__init__.py /app/util/__init__.py
COPY util/constants.py  /app/util/constants.py
COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 8080

CMD python app.py
