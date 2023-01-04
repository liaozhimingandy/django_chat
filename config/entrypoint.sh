#!/bin/sh

python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py makemigrations user
python manage.py migrate

exec "$@"

gunicorn django_welink.wsgi:application -c /opt/app/config/gunicorn.py
# 文件编码必须是unix; set ff=unix
