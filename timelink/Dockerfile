FROM python:3.7-slim

WORKDIR /usr/src/timelink_web
COPY requirements.txt .
RUN pip install -r requirements.txt 

COPY . .