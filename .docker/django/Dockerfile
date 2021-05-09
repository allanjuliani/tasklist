# https://hub.docker.com/_/python
FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends
RUN apt-get install default-libmysqlclient-dev build-essential -y

RUN python3 -m pip install --upgrade pip

RUN useradd -ms /bin/bash ubuntu

USER ubuntu

COPY . /home/ubuntu/tasklist

WORKDIR /home/ubuntu/tasklist

RUN pip install -r requirements.txt

ENTRYPOINT [".docker/django/entrypoint.sh"]
