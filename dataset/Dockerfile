FROM python:3.9.4-slim

COPY one-million-reddit-confessions.csv one-million-reddit-confession.csv
COPY loaddata.py loaddata.py
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ENV DB_NAME=${DB_NAME}
ENV DB_HOST=${DB_HOST}
ENV DB_PASSWORD=${DB_PASSWORD}
ENV DB_USER=${DB_USER}

CMD python loaddata.py