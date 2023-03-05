FROM python:3.10.0-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/code/src"

WORKDIR /code

COPY requirements/main.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY src /code/src
COPY .env /code/.env
COPY migrations /code/migrations
COPY pyproject.toml /code/pyproject.toml
