import uuid

from django.db import models
from django.utils.timezone import now
from django.conf import settings

from account.models import Account
from oauth.models import App


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

    content = models.JSONField(help_text="内容", db_comment='内容', verbose_name="内容")
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, help_text="用户ID", db_comment='用户ID',
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
    app = models.ForeignKey(App, on_delete=models.PROTECT, db_comment="帖子所属应用", verbose_name="帖子所属应用",
                            help_text="帖子所属应用", db_index=True)
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
    image_md5 = models.CharField('图片md值', db_default='', max_length=32, db_comment="图片md值", unique=True,
                                 null=True)
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
