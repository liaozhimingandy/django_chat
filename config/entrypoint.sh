#!/bin/sh

python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py makemigrations user
python manage.py migrate

exec "$@"
# 文件编码必须是unix; set ff=unix
