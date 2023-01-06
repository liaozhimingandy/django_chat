from django.contrib import admin
from user.models import User
from django.contrib.auth.admin import UserAdmin

# 自定义主题
admin.site.site_header = "后台管理系统"
admin.site.site_title = "后台管理系统"
admin.site.index_title = "后台管理系统"


# Register your models here.
@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ["uid", "username", "nick_name", "last_login"]
    exclude = ['gmt_created', ]
    readonly_fields = ('uid', 'id', 'gmt_created', 'login_ip')
    # 搜索
    search_fields = ['uid', "user_name"]
    # 分页 - 设置每页最大显示数目
    list_per_page = 10

    # 后台显示的字段
    fieldsets = [
        (None, {'fields': ['username', 'password', 'uid', 'is_staff', 'is_superuser']}),
        ('用户活跃信息', {'fields': ['nick_name', 'mobile', 'sex', 'avatar', 'user_status', 'user_type',
                                     'login_ip', 'email', 'gmt_created']}),
    ]
