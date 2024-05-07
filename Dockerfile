# 定义镜像的标签
ARG TAG=3.11.2-slim-buster

FROM python:${TAG} as builder-image

# pip镜像源
ENV PIPURL "https://mirrors.aliyun.com/pypi/simple/"

# change apt-get mirror
COPY pdm.lock .

# 安装依赖包
RUN pip3 install --no-cache-dir pdm -i ${PIPURL} --default-timeout=1000 \
    && pdm export -o requirements.txt  --without-hashes \
    && pip3 install --no-cache-dir -r requirements.txt -i ${PIPURL} --default-timeout=1000 \
    && rm -f requirements.txt \
    && rm -f pdm.lock



FROM python:${TAG}

# 如果python大版本有调整,请调整python的路径,示例: 3.11 -> 调整为对应版本
COPY --from=builder-image /usr/local/bin /usr/local/bin
COPY --from=builder-image /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

RUN mkdir /opt/app
COPY . /opt/app

WORKDIR /opt/app
# command
CMD ["gunicorn", "django_chat.wsgi:application", "-c", "/opt/app/config/gunicorn.py"]

# 构建命令
# docker build -t liaozhiming/django_chat:latest .
# 文件格式问题,请保持unix编码;set ff=unix
