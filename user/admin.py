from django.contrib import admin
from user.models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["uid", "username"]
    exclude = ['gmt_created', ]
    # 搜索
    search_fields = ['uid']
    # 分页 - 设置每页最大显示数目
    list_per_page = 10
