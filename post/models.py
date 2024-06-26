import uuid

from django.db import models
from django.db.models import UniqueConstraint
from django.utils.timezone import now
from django.conf import settings


# Create your models here.
class Post(models.Model):
    class RightStatusChoice(models.IntegerChoices):
        PUBLIC = (1, "公开")
        PRIVATE = (2, "仅自己")

    class FromDeviceChoice(models.IntegerChoices):
        WEB = (1, "网页版")
        ANDROID = (2, "安卓端")
        IOS = (3, "IPHONE")
        UNKNOWN = (9, "未知")

    class ContentClassChoice(models.IntegerChoices):
        TextElem = (1, "普通")

    post_id = models.UUIDField(help_text="帖子ID", db_comment='帖子ID', verbose_name="帖子ID", default=uuid.uuid4,
                               editable=False)
    content = models.JSONField(help_text="内容", db_comment='内容', verbose_name="内容")
    account_id = models.CharField(max_length=7, help_text="用户ID", db_comment='用户ID',
                                  verbose_name="用户ID", null=True, blank=True)
    from_ip = models.GenericIPAddressField(help_text="来源ip", db_comment="来源ip", verbose_name="用户ID",
                                           unpack_ipv4=True)
    from_device = models.PositiveSmallIntegerField(choices=FromDeviceChoice, help_text='来源设备名称',
                                                   db_comment='来源设备名称', verbose_name="来源设备名称")
    right_status = models.PositiveSmallIntegerField(help_text='权限状态', default=1, db_comment="权限状态",
                                                    db_default=1, choices=RightStatusChoice, verbose_name="权限状态")
    location = models.CharField(null=True, blank=True, help_text="位置", max_length=64,
                                db_comment="位置", verbose_name="位置")
    is_top = models.BooleanField(default=False, help_text='是否置顶', db_comment='是否置顶', db_default=False,
                                 verbose_name="是否置顶")
    content_class = models.PositiveSmallIntegerField(help_text='内容类型', default=1, null=False, blank=True,
                                                     db_comment="内容类型", choices=ContentClassChoice)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, help_text="经度", db_comment="经度", null=True,
                                   blank=True, verbose_name="经度")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, help_text="纬度", db_comment="纬度", null=True,
                                    blank=True, verbose_name="纬度")
    status = models.SmallIntegerField("帖子状态", help_text="帖子状态", db_comment="帖子状态", default=0)
    gmt_created = models.DateTimeField(auto_now_add=True, help_text="创建日期时间", db_comment="创建日期时间")

    def __str__(self):
        return f"{self.id}"

    # 表信息声明
    class Meta:
        # 设置数据库中表名
        db_table = f"{settings.APP_NAME}_post"
        verbose_name = "帖子表"
        verbose_name_plural = verbose_name


class Image(models.Model):
    image_name = models.CharField('图片名称', null=True, db_comment='图片名称', db_default='', max_length=128)
    image = models.ImageField("图片", upload_to='images')
    image_md5 = models.UUIDField('图片md值',  db_comment="图片md值", unique=True, null=True)
    gmt_created = models.DateTimeField('记录日期', auto_now_add=True, db_default=now())

    class Meta:
        # 设置数据库中表名
        db_table = f"{settings.APP_NAME}_image"
        verbose_name = "图片表"
        verbose_name_plural = verbose_name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.image_name = self.image.name
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.image.url


class Like(models.Model):
    post_id = models.UUIDField(verbose_name="帖子ID", db_comment="帖子ID", help_text="帖子ID")
    account_id = models.CharField(max_length=7, verbose_name="赞的人", help_text="赞的人",
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
            UniqueConstraint(fields=['post_id', 'account_id'], name='uk_like')
        ]


class Comment(models.Model):
    comment_id = models.UUIDField(db_comment="评论ID", help_text="评论ID", unique=True, db_index=True, default=uuid.uuid4,
                                  editable=False)
    is_root = models.BooleanField("是否为一级评论", default=True, help_text="是否为一级评论",
                                  db_comment="是否为一级评论", db_default=True)
    parent_id = models.UUIDField(help_text="父评论", db_comment="父评论", null=True, db_default=None)
    content = models.TextField("内容", db_comment="评论内容", help_text="评论内容")
    account_id = models.CharField(max_length=7, verbose_name="评论者", help_text="评论者ID", db_comment="评论者")
    post_id = models.UUIDField(verbose_name="内容ID", db_comment="内容", help_text="post_id", db_index=True)
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