from django.contrib import admin

from account.models import Account


# Register your models here.
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'nick_name', "sex")
    exclude = ['gmt_created', ]
    # 搜索
    search_fields = ['username']
    # 分页 - 设置每页最大显示数目
    list_per_page = 10