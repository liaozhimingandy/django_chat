#!/bin/sh

python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate

set -e

# 设置Django环境变量
export DJANGO_SETTINGS_MODULE=django_chat.settings

# 检查是否已设置环境变量
if [ -z "$DJANGO_SUPERUSER_USERNAME" ] || [ -z "$DJANGO_SUPERUSER_EMAIL" ] || [ -z "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "Error: DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, and DJANGO_SUPERUSER_PASSWORD must be set."
    exit 1
fi

# 检查是否有管理员用户，如果没有则创建
python manage.py shell <<EOF
from django.contrib.auth.models import User
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')
    print("Superuser created successfully.")
else:
    print("Superuser already exists.")
EOF

# use Gunicorn to start app
exec gunicorn django_chat.wsgi:application -c /opt/app/config/gunicorn.py
# 文件编码必须是unix; set ff=unix
