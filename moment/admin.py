from django.contrib import admin

from django_welink import settings
from moment.models import Moment, Image


# Register your models here.
@admin.register(Moment)
class MomentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'content', 'liked', 'gmt_created']
    exclude = ['-gmt_created', ]
    # 搜索
    search_fields = ['user_id']
    # 分页 - 设置每页最大显示数目
    list_per_page = 10


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ["id", 'image_name', "image_md5", 'gmt_created']


admin.AdminSite.site_header = format(f'后台管理{settings.APP_VERSION_VERBOSE}')
