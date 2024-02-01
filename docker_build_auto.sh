#!/bin/bash

# 获取当前 Git 哈希值
GIT_HASH=$(git rev-parse --short HEAD)

# 构建 Docker 镜像，并将 Git 哈希值作为标签的一部分
docker build -t chatapp:${GIT_HASH}