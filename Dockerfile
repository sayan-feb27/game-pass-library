FROM python:3.10.0-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code/src
COPY .env /code/.env
COPY migrations /code/migrations
COPY pyproject.toml /code/pyproject.toml

ENV PYTHONPATH "${PYTHONPATH}:/code/src"

CMD ["uvicorn", "src.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]
