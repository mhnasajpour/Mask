FROM python:3.10.6-alpine3.16

WORKDIR /code

COPY requirements.txt .

RUN apk update && apk add python3-dev gcc libc-dev

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000