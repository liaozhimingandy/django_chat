from django.db import models
from django.conf import settings


# Create your models here.
class Comment(models.Model):
    is_root = models.BooleanField("是否为一级评论", default=True, help_text="是否为一级评论",
                                  db_comment="是否为一级评论", db_default=True)
    pid = models.PositiveBigIntegerField("父评论ID", db_comment="父评论ID", help_text="父评论ID",
                                         null=True, db_default=None)
    content = models.TextField("内容", db_comment="评论内容", help_text="评论内容")
    uid = models.PositiveBigIntegerField(verbose_name="评论者ID", help_text="评论者ID", db_comment="评论者ID")
    app_id = models.PositiveIntegerField(verbose_name="所属应用ID", db_comment="所属应用ID", help_text="所属应用ID",
                                         db_index=True)
    post_id = models.PositiveBigIntegerField(verbose_name="内容ID", db_comment="内容ID",
                                             help_text="内容ID", db_index=True)
    gmt_created = models.DateTimeField(auto_now_add=True, help_text="创建日期时间", db_comment="创建日期时间",
                                       verbose_name="创建日期时间")

    # 表信息声明
    class Meta:
        db_table = f'{settings.APP_NAME}_comment'
        # 设置数据库中表名
        verbose_name = "评论表"
        verbose_name_plural = verbose_name
