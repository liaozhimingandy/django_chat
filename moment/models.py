from django.db import models


# Create your models here.
class Moment(models.Model):
    moment_id = models.AutoField(primary_key=True)
    moment = models.CharField(null=False, blank=False, help_text="动态内容", max_length=1024)
    user_id = models.CharField(default=None, help_text="所属用户id", max_length=1024)
    loc = models.CharField(default='', help_text="位置", max_length=1024)
    gmt_created = models.DateTimeField(auto_now=True, help_text="创建日期时间")
    from_ip = models.GenericIPAddressField(null=False, blank=False, help_text="来源ip")
    liked = models.PositiveIntegerField(null=False, blank=False, default=0, help_text='赞数')
    content_class = models.PositiveSmallIntegerField(help_text='内容类型')
    from_device = models.CharField(max_length=512, null=False, blank=False, help_text='来源设备名称')
    right_status = models.PositiveSmallIntegerField(help_text='权限状态')

    # 表信息声明
    class Meta:
        # 设置数据库中表名
        db_table = "wl_moment"
        verbose_name = "动态表"
        verbose_name_plural = verbose_name

