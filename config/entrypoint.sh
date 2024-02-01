#!/bin/sh

python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate
# auto create admin user
python manage.py createsuperuser --noinput
python manage.py makemigrations moment
python manage.py migrate moment

# auto create admin user
# echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@alsoapp.com', 'zhiming')" | python manage.py shell

exec "$@"
# 文件编码必须是unix; set ff=unix
