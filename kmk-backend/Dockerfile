FROM python:3.9-slim-buster

WORKDIR /app

USER root
ENV PYTHONUNBUFFERED 1

COPY ./Pipfile .
COPY ./Pipfile.lock .
COPY . .

RUN pip3 install pipenv
RUN pipenv install --deploy --clear --system --ignore-pipfile

ENTRYPOINT ["bash", "/app/kmk-backend/docker-entrypoint.sh"]
