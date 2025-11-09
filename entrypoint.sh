#!/bin/sh

# Set options and positional parameters 
# (from https://www.ibm.com/docs/en/zos/3.2.0?topic=descriptions-set-set-unset-command-options-positional-parameters)
# - -o: 
#     - Sets a shell flag.
# - errexit:
#     - Tells a noninteractive shell to execute the ERR trap and then exit. This flag is disabled when reading 
#       profiles.
# - tracex:
#     - Prints commands and their arguments as they run.
set -o errexit
set -o tracex

# (from https://docs.djangoproject.com/en/4.2/ref/django-admin/#migrate)
python manage.py migrate

# (from https://docs.djangoproject.com/en/4.2/ref/django-admin/#runserver)
python manage.py runserver 0.0.0.0:8080"