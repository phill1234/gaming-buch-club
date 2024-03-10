#!/bin/bash

if [ "$1" == "run" ]; then
  echo "Running backend"
  poetry run python manage.py collectstatic --noinput
  poetry run python manage.py migrate --noinput --settings project.settings
  poetry run uvicorn project.asgi:app --host "0.0.0.0" --port 8000
fi

if [ "$1" == "migrate" ]; then
  echo "Running migrations"
  poetry run python manage.py migrate --noinput --settings project.settings
fi


if [ "$1" == "test" ]; then
  echo "Running tests"
  poetry install
  poetry run pytest
fi
