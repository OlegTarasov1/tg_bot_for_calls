FROM python:3.13-bookworm

RUN apt install make

WORKDIR /app

COPY ./requirements.txt .

RUN pip install -r requirements.txt

# RUN make migrate

COPY ./src .
