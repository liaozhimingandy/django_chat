FROM python:3.10.6-slim-buster as builder-image

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

FROM python:3.10.6-slim-buster

COPY --from=builder-image /usr/local/bin /usr/local/bin
COPY --from=builder-image /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

RUN mkdir /opt/app
WORKDIR /opt/app
COPY . /opt/app

RUN ["chmod", "+x", "/opt/app/config/entrypoint.sh"]

# run entrypoint.sh
ENTRYPOINT ["/opt/app/config/entrypoint.sh"]
