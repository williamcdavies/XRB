#!/bin/bash

python manage.py collectstatic --noinput

python manage.py makemigrations
python manage.py migrate

# start Gunicorn to host django REST API and admin interface
gunicorn config.wsgi:application --bind 0.0.0.0:8000 &

# start Django FTP server
python manage.py ftpserver 0.0.0.0:10021
