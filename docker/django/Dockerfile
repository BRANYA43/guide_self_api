FROM python:3.11-slim
LABEL authors="BRANYA43 bogdan.timchenko.2504@gmail.com"


RUN apt-get update; \
    apt-get install -y --no-install-recommends build-essential libpq-dev gcc mc nano curl; \
    rm -rf /var/lib/apt/lists/*; \
    python -m venv /opt/.venv

ENV PATH="/opt/venv/bin:$PATH" PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 DOCKER_RUN=1

WORKDIR /opt/src/

COPY pyproject.toml ../

RUN pip install --upgrade pip; \
    pip install poetry --no-cache-dir; \
    poetry install; \
    poetry export -f requirements.txt --without-hashes --output requirements.txt; \
    pip install -r requirements.txt --no-cache-dir; \
    pip install psycopg --no-cache-dir; \
    rm requirements.txt

COPY /src .
