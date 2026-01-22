#!/bin/bash

python manage.py collectstatic --noinput

python manage.py makemigrations api
python manage.py migrate api

gunicorn --bind 0.0.0.0:8000 config.wsgi:application
