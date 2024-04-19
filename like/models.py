from django.contrib.auth.models import User
from django.db import models
from django.db.models import UniqueConstraint
from django.conf import settings


# Create your models here.
class Like(models.Model):
    app_id = models.CharField(max_length=36, verbose_name="所属应用ID", db_comment="所属应用ID", help_text="所属应用ID")
    post_id = models.CharField(max_length=36, verbose_name="内容ID", db_comment="内容ID", help_text="内容ID")
    uid = models.CharField(max_length=36, verbose_name="赞的人", help_text="赞的人", db_comment="赞的人")
    gmt_created = models.DateTimeField(auto_now_add=True, help_text="创建日期时间", db_comment="创建日期时间",
                                       verbose_name="创建日期时间")

    # 表信息声明
    class Meta:
        db_table = f'{settings.APP_NAME}_like'
        # 设置数据库中表名
        verbose_name = "赞表"
        verbose_name_plural = verbose_name
        constraints = [
            UniqueConstraint(fields=['app_id', 'post_id', 'uid'], name='uk_like')
        ]
