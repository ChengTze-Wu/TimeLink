FROM python:3.12-slim

WORKDIR /usr/src
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    rm requirements.txt

COPY app app

EXPOSE 8800
ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8800"]
