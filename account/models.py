import uuid
from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models

from django.conf import settings


def salt_default():
    return uuid.uuid4().hex[:8]


def username_default():
    return f"cid_{uuid.uuid4().hex[:7]}"


# Create your models here.
class Account(models.Model):
    class SexChoices(models.IntegerChoices):
        Other = (0, "未知的性别")
        Male = (1, "男性")
        Female = (2, "女性")
        Unknown = (9, "未说明的性别")

    class AreaCodeChoices(models.TextChoices):
        CHN = ('CHN', '中国')

    username = models.CharField(default=username_default, max_length=32, unique=True, db_comment="用户名",
                                help_text="用户名", verbose_name="用户名", db_index=True)
    nick_name = models.CharField(max_length=64, db_comment="昵称", help_text="昵称", verbose_name="昵称")
    email = models.EmailField(db_comment="电子邮箱", help_text="电子邮箱", verbose_name="电子邮箱",
                              null=True, db_index=True)
    gmt_birth = models.DateTimeField(db_comment="出生日期", help_text="出生日期", verbose_name="出生日期", null=True,
                                     blank=True)
    areaCode = models.CharField(choices=AreaCodeChoices, max_length=3, db_comment="区域代码", help_text="区域代码",
                                verbose_name="区域代码", db_default='CHN', default='CHN', null=True)
    mobile = models.CharField(max_length=32, db_comment="电话号码", help_text="电话号码", verbose_name="电话号码",
                              null=True, db_index=True, blank=True)
    sex = models.SmallIntegerField(choices=SexChoices, db_comment="性别", help_text="性别", verbose_name="性别",
                                   db_default=0, default=0)
    avatar = models.URLField(db_comment="头像链接", help_text="头像链接", verbose_name="头像链接",
                             db_default='https://www.alsoapp.com/favicon.svg',
                             default='https://www.alsoapp.com/favicon.svg')
    is_active = models.BooleanField(db_default=True, default=True, db_comment="账户状态", help_text="账户状态",
                                    verbose_name="账户状态")
    user_type = models.SmallIntegerField(db_comment="账户状态", help_text="账户状态", verbose_name="账户状态",
                                         default=1)
    password = models.CharField(max_length=128, db_comment="用户密码", help_text="用户密码", verbose_name="用户密码")
    allow_add_friend = models.BooleanField(db_default=True, default=True, db_comment="允许添加好友",
                                           help_text="允许添加好友", verbose_name="允许添加好友")
    allow_beep = models.BooleanField(db_default=True, default=True, db_comment="是否允许提示音",
                                     help_text="是否允许提示音", verbose_name="是否允许提示音")
    allow_vibration = models.BooleanField(db_default=True, default=True, db_comment="是否允许震动提示",
                                          help_text="是否允许震动提示", verbose_name="是否允许震动提示")
    gmt_created = models.DateTimeField(auto_now_add=True, help_text="创建日期时间", db_comment="创建日期时间",
                                       verbose_name="创建日期时间")
    im_id = models.CharField(max_length=64, db_comment="im ID", help_text="im ID", verbose_name="im ID", null=True,
                             blank=True)
    salt = models.CharField(default=salt_default, max_length=8, db_comment="盐", help_text="盐")
    gmt_modified = models.DateTimeField(auto_now=True, help_text="最后修改时间", db_comment="最后修改时间",
                                        verbose_name="最后修改时间")

    def clean(self):
        if self.email is not None:
            # 如果字段不为空，检查其在表中是否已存在
            if Account.objects.exclude(pk=self.pk).filter(email=self.email).exists():
                raise ValidationError({'email': '字段必须唯一'})
        if self.username is not None:
            # 如果字段不为空，检查其在表中是否已存在
            if Account.objects.exclude(pk=self.pk).filter(username=self.username).exists():
                raise ValidationError({'username': '字段必须唯一'})

    # 表信息声明
    class Meta:
        db_table = f'{settings.APP_NAME}_account'
        # 设置数据库中表名
        verbose_name = "用户信息表"
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        # 在保存之前先执行验证
        self.full_clean()
        super().save(*args, **kwargs)
