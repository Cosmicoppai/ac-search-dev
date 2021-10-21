#!/usr/bin/env sh

set -e

python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py makemigrations app
python manage.py migrate
python manage.py runserver 0.0.0.0:9000