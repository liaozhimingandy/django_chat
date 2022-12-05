from django.contrib import admin
from moment.models import Moment


# Register your models here.
@admin.register(Moment)
class MomentAdmin(admin.ModelAdmin):
    list_display = ['moment_id', 'user_id', 'liked', 'moment']
    exclude = ['gmt_created', ]
    # 搜索
    search_fields = ['user_id']
    # 分页 - 设置每页最大显示数目
    list_per_page = 10
