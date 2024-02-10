FROM python:3.12-slim

WORKDIR /usr/src
COPY requirements.txt .
RUN apt-get update && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf requirements.txt && \
    rm -rf /var/lib/apt/lists/*

COPY gunicorn.conf.py .
COPY app app

EXPOSE 8000
ENTRYPOINT ["gunicorn"]
