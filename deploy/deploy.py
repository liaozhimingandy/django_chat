#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""=================================================
    @Project: django_hip_service
    @File： deploy.py
    @Author：liaozhimingandy
    @Email: liaozhimingandy@gmail.com
    @Date：2024-03-20 9:48
================================================="""
from dataclasses import dataclass
from pathlib import Path
import subprocess


@dataclass
class DeployBot:
    name: str = "DeployBot"

    def _deploy_docker_image(self, image_name: str, dockerfile_path: Path) -> None:
        cmd_docker_build = ["docker", "build", "-t", image_name, dockerfile_path]
        subprocess.run(cmd_docker_build)
        print(f"{self.name}自动构建成功!docker镜像: {image_name}\n")

    def _deploy_docker_push(self, image_name: str) -> None:
        # 自动提交至阿里云镜像仓库
        image_src = "registry.cn-hangzhou.aliyuncs.com/liaozhiming"
        image_tag_remote = f"{image_src}/{image_name}"
        cmd_docker_tag = ["docker", "tag", image_name, image_tag_remote]
        cmd_docker_push = ["docker", "push", image_tag_remote]
        cmd_docker_untag = ["docker", "rmi", image_tag_remote]

        subprocess.run(cmd_docker_tag)
        subprocess.run(cmd_docker_push)
        subprocess.run(cmd_docker_untag)

        print(f"{self.name}docker镜像push成功,{image_name}\n")

    def _deploy_docker_env(self, **kwargs) -> None:
        """
        覆盖或赋值环境变量对应值
        :param kwargs:
        :return:
        """

        # 读取.env文件中的变量
        env_values = {}
        with open('../config/.env', 'r', encoding="UTF-8") as fp:
            for line in fp:
                if line.strip() and not line.strip().startswith('#'):
                    key, value = line.strip().split('=', 1)
                    env_values[key.strip()] = value.strip()

        # 设置新的变量值
        env_values.update(**kwargs)

        # 回写到.env文件中
        with open('../.env', 'w', encoding="UTF-8") as fp:
            for key, value in env_values.items():
                fp.write(f"{key}={value}\n")

        print(f".env更新成功!")

    def deploy(self):
        # 使用git命令获取简短hash值
        cmd_git_hash = ["git", "rev-parse", "--short", "HEAD"]
        # 使用git命令获取当前分支
        cmd_git_branch = ["git", "rev-parse", "--abbrev-ref", "HEAD"]

        desc_git_hash = subprocess.check_output(cmd_git_hash).strip().decode('utf-8')
        desc_git_branch = subprocess.check_output(cmd_git_branch).strip().decode('utf-8')

        # 覆盖AppVersionHash文件
        with open('../AppVersionHash.txt', 'w') as fp:
            fp.writelines(desc_git_hash)

        from django_chat import settings
        app_version = settings.__version__
        image_name = f"django_chat:{app_version}"
        dockerfile_path = Path(__file__).resolve().parent.parent

        # docker构建镜像命令
        self._deploy_docker_image(image_name=image_name, dockerfile_path=dockerfile_path)

        # 更新.env变量
        self._deploy_docker_env(APP_IMAGE=image_name, APP_COMMIT_HASH=desc_git_hash)

        # 自动提交至阿里云镜像仓库
        self._deploy_docker_push(image_name=image_name)

        print(
            f"自动构建成功!version: {app_version}, revision: {desc_git_branch}-{desc_git_hash}, docker镜像: {image_name}\n")


if __name__ == '__main__':
    bot = DeployBot()
    bot.deploy()
