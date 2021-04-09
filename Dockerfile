FROM python:3.8-alpine

WORKDIR /Portfolio_website_flask

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY .env .env
COPY app app
#COPY migrations migrations
COPY app.db app.db
COPY main.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP=main.py

EXPOSE 5000

ENTRYPOINT ["sh","./boot.sh"]