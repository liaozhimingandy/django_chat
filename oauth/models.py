import uuid

from django.db import models
from django.core.management.utils import get_random_string
from django.conf import settings


def salt_default():
    return uuid.uuid4().hex[:8]


def app_id_default():
    return uuid.uuid4().hex[:5]


def app_secret_default():
    return get_random_string(32)


# Create your models here.
class App(models.Model):
    id = models.CharField(max_length=5, default=app_id_default, db_comment="appid", editable=False, primary_key=True)
    app_secret = models.CharField(default=app_secret_default, max_length=32, db_comment="应用密钥",
                                  help_text="应用密钥")
    salt = models.CharField(default=salt_default, max_length=8, db_comment="盐", help_text="盐")
    app_name = models.CharField("应用名称", max_length=32, db_comment="应用名称", help_text="应用名称")
    app_en_name = models.CharField("应用英文名称", max_length=64, db_comment="应用英文名称", help_text="应用英文名称",
                                   null=True, blank=True)
    is_active = models.BooleanField("激活状态", default=True, db_comment="激活状态", help_text="激活状态", db_default=True)
    gmt_created = models.DateTimeField("创建日期时间", auto_now_add=True, help_text="创建日期时间",
                                       db_comment="创建日期时间")
    gmt_updated = models.DateTimeField("最后更新日期时间", auto_now=True, help_text="最后更新日期时间",
                                       db_comment="最后更新日期时间")

    def __str__(self):
        return f"{self.app_name}-{settings.PREFIX_ID}{self.id}"

    class Meta:
        db_table = f"{settings.APP_NAME}_app"
        verbose_name = "应用信息"
        verbose_name_plural = verbose_name
