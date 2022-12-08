from django.contrib import admin
from moment.models import Moment


# Register your models here.
@admin.register(Moment)
class MomentAdmin(admin.ModelAdmin):
    list_display = ['mid', 'uid', 'liked', 'moment']
    exclude = ['gmt_created', ]
    # 搜索
    search_fields = ['uid']
    # 分页 - 设置每页最大显示数目
    list_per_page = 10
