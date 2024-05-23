import uuid

from django.db import models
from django.conf import settings

from account.models import Account
from oauth.models import App
from post.models import Post


# Create your models here.
class Comment(models.Model):
    comment_id = models.UUIDField(db_comment="评论ID", help_text="评论ID", unique=True, db_index=True, default=uuid.uuid4,
                                  editable=False)
    is_root = models.BooleanField("是否为一级评论", default=True, help_text="是否为一级评论",
                                  db_comment="是否为一级评论", db_default=True)
    parent_id = models.UUIDField(help_text="父评论", db_comment="父评论", null=True, db_default=None)
    content = models.TextField("内容", db_comment="评论内容", help_text="评论内容")
    account_id = models.CharField(max_length=7, verbose_name="评论者", help_text="评论者ID", db_comment="评论者",
                                  null=True, blank=True)
    app_id = models.CharField(max_length=5, verbose_name="所属应用", db_comment="所属应用", help_text="所属应用",
                              db_index=True, default='1')
    post_id = models.UUIDField(verbose_name="内容", db_comment="内容", help_text="内容", db_index=True)
    gmt_created = models.DateTimeField(auto_now_add=True, help_text="创建日期时间", db_comment="创建日期时间",
                                       verbose_name="创建日期时间")

    def __str__(self):
        return f'{self.id}'

    # 表信息声明
    class Meta:
        db_table = f'{settings.APP_NAME}_comment'
        # 设置数据库中表名
        verbose_name = "评论表"
        verbose_name_plural = verbose_name
