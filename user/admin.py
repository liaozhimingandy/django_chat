from django.contrib import admin
from user.models import User

# 自定义主题
admin.site.site_header = "后台管理系统"
admin.site.site_title = "后台管理系统"
admin.site.index_title = "后台管理系统"


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["uid", "username", "nick_name"]
    exclude = ['gmt_created', ]
    readonly_fields = ('uid', 'id')
    # 搜索
    search_fields = ['uid', "user_name"]
    # 分页 - 设置每页最大显示数目
    list_per_page = 10
