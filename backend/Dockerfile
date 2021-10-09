FROM python:3.9-slim-buster

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ARG ENV

COPY . .
COPY ./Pipfile .
COPY ./Pipfile.lock .

RUN pip3 install pipenv==2021.5.29
RUN if [ "$ENV" = "dev" ]; then \
    pipenv install --dev --deploy --clear --system --ignore-pipfile; \
else \
    pipenv install --deploy --clear --system --ignore-pipfile; \
fi

ENTRYPOINT ["bash", "/app/backend/docker-entrypoint.sh"]
