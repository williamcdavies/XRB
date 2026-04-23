#!/bin/bash

python manage.py collectstatic --noinput

python manage.py makemigrations
python manage.py migrate

python manage.py regenerate_authorized_keys || true

gunicorn --bind 0.0.0.0:8000 config.wsgi:application
