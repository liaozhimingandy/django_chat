from django.db import models


# Create your models here.
class Moment(models.Model):
    mid = models.AutoField(primary_key=True)
    moment = models.CharField(null=False, blank=False, help_text="动态内容", max_length=1024, verbose_name='动态内容')
    uid = models.CharField(default='', help_text="所属用户id", max_length=32)
    loc = models.CharField(null=True, blank=True, default='', help_text="位置", max_length=128)
    gmt_created = models.DateTimeField(auto_now=True, help_text="创建日期时间")
    from_ip = models.GenericIPAddressField(null=False, blank=False, help_text="来源ip")
    liked = models.PositiveIntegerField(null=True, blank=True, default=0, help_text='赞数')
    content_class = models.PositiveSmallIntegerField(help_text='内容类型', default=1, null=False, blank=True)
    from_device = models.CharField(max_length=64, null=False, blank=False, help_text='来源设备名称')
    right_status = models.PositiveSmallIntegerField(help_text='权限状态', null=False, blank=False, default=0)
    address = models.CharField(max_length=128, null=True, blank=True, help_text='地址名称', default='')
    is_top = models.BooleanField(default=False, null=False, blank=False, help_text='是否置顶')
    images = models.JSONField(null=True, help_text='图片列表')
    videos = models.JSONField(null=True, help_text='视频列表')
    poi = models.CharField(max_length=64, null=True, blank=True, help_text='地址POI信息', default='')

    # 表信息声明
    class Meta:
        # 设置数据库中表名
        db_table = "wl_moment"
        verbose_name = "动态表"
        verbose_name_plural = verbose_name
        ordering = ['-mid', ]
