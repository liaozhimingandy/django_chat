from django.db import models
from django.utils.timezone import now


# Create your models here.
class Moment(models.Model):
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

    content = models.CharField(null=True, blank=True, help_text="动态内容", max_length=1024, db_comment='动态内容',
                               db_default='')
    user_id = models.CharField(db_default='', help_text="所属用户id", max_length=32, db_comment='所属用户id')
    location = models.CharField(null=True, blank=True, db_default='', help_text="位置", max_length=128, db_comment="位置")
    from_ip = models.GenericIPAddressField(help_text="来源ip", db_comment="来源ip")
    liked = models.PositiveIntegerField(default=0, help_text='赞数', db_comment="赞数")
    content_class = models.PositiveSmallIntegerField(help_text='内容类型', default=1, null=False, blank=True,
                                                     db_comment="内容类型", choices=ContentClassChoice)
    from_device = models.PositiveSmallIntegerField(choices=FromDeviceChoice, help_text='来源设备名称',
                                                   db_comment='来源设备名称')
    right_status = models.PositiveSmallIntegerField(help_text='权限状态', default=1, db_comment="权限状态",
                                                    db_default=1, choices=RightStatusChoice)
    is_top = models.BooleanField(default=False, help_text='是否置顶', db_comment='是否置顶', db_default=False)
    images = models.JSONField(null=True, blank=True, help_text='图片列表', db_comment='图片列表')
    videos = models.JSONField(null=True, blank=True, help_text='视频列表', db_comment='视频列表')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, help_text="经度", db_comment="经度", null=True,
                                   blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, help_text="纬度", db_comment="纬度", null=True,
                                    blank=True)
    gmt_created = models.DateTimeField(auto_now_add=True, help_text="创建日期时间", db_comment="创建日期时间")

    # 表信息声明
    class Meta:
        # 设置数据库中表名
        db_table = "welink_moment"
        verbose_name = "动态表"
        verbose_name_plural = verbose_name


class Image(models.Model):
    image_name = models.CharField('图片名称', null=True, db_comment='图片名称', db_default='', max_length=128)
    image = models.ImageField("图片", upload_to='images')
    image_md5 = models.CharField('图片md值', db_default='', max_length=32, db_comment="图片md值", unique=True, null=True)
    gmt_created = models.DateTimeField('记录日期', auto_now_add=True, db_default=now())

    class Meta:
        # 设置数据库中表名
        db_table = "welink_image"
        verbose_name = "图片表"
        verbose_name_plural = verbose_name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.image_name = self.image.name
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.image.url















