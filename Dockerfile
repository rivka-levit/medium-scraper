FROM python:3.12
LABEL authors="Rivka Levit"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app

WORKDIR /app

EXPOSE 80

RUN python -m pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /tmp