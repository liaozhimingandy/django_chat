FROM python:3.10.6-slim-buster

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install -U pip setuptools wheel -i https://mirrors.aliyun.com/pypi/simple/ || \
    pip install -U pip setuptools wheel

RUN mkdir /opt/app
WORKDIR /opt/app
COPY . /opt/app

RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt || \
    pip install -r requirements.txt 

RUN ["chmod", "+x", "/opt/app/config/entrypoint.sh"]

CMD ["gunicorn", "django_welink.wsgi:application", "-c", "/opt/app/config/gunicorn.conf"]
# run entrypoint.sh
#ENTRYPOINT ["/opt/app/config/entrypoint.sh"]
