FROM python:3.12-slim

WORKDIR /usr/src
COPY requirements.txt .

# Set the environment variable to install multidict on 
# another operating system (or Alpine Linux inside a Docker)
# See: https://pypi.org/project/multidict/#library-installation
ENV MULTIDICT_NO_EXTENSIONS=1

ENV TZ=Asia/Taipei

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf requirements.txt && \
    rm -rf /var/lib/apt/lists/*

COPY app app

EXPOSE 8000
ENV PORT 8000
ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
