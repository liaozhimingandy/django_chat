from django.contrib.auth.models import User
from django.db import models
from django.db.models import UniqueConstraint
from django.conf import settings

from account.models import Account
from oauth.models import App
from post.models import Post


# Create your models here.
class Like(models.Model):
    app = models.ForeignKey(App, on_delete=models.PROTECT, verbose_name="所属应用", db_comment="所属应用",
                            help_text="所属应用")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="内容", db_comment="内容", help_text="内容")
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, verbose_name="赞的人", help_text="赞的人",
                                db_comment="赞的人", null=True, blank=True)
    gmt_created = models.DateTimeField(auto_now_add=True, help_text="创建日期时间", db_comment="创建日期时间",
                                       verbose_name="创建日期时间")

    # 表信息声明
    class Meta:
        db_table = f'{settings.APP_NAME}_like'
        # 设置数据库中表名
        verbose_name = "赞表"
        verbose_name_plural = verbose_name
        constraints = [
            UniqueConstraint(fields=['app', 'post', 'account'], name='uk_like')
        ]
