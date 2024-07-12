FROM python:3.11-alpine3.18
LABEL maintainer='tiomashimon'

ENV PYTHONUNBUFFERED 1

# Install bash and other necessary packages
RUN apk update && apk add bash

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; \
        then pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser --disabled-password --no-create-home django-user


USER django-user


