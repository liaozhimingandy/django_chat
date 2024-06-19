from django.contrib import admin

from django.conf import settings

from account.models import Account, App


# Register your models here.
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display_links = ["display_username", ]
    exclude = ['gmt_created', ]
    # 搜索
    search_fields = ['display_username']
    # 分页 - 设置每页最大显示数目
    list_per_page = 10
    readonly_fields = ["display_username", ]

    def get_list_display(self, request):
        """返回要显示的字段列表"""
        list_display = ["display_username", ]
        for field in Account._meta.fields:
            if field.name in ("username", "id"):
                continue
            list_display.append(field.name)
        return list_display

    def display_username(self, obj):
        return f"{settings.PREFIX_ID}{obj.username}"

    display_username.short_description = "用户名"


@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display_links = ["display_id", ]
    # list_display = [field.name for field in App._meta.fields]
    readonly_fields = ["salt", "display_id", ]

    def display_id(self, obj):
        return f"{settings.PREFIX_ID}{obj.app_id}"

    def get_list_display(self, request):
        """返回要显示的字段列表"""
        list_display = ["display_id", ]
        for field in App._meta.fields:
            if field.name in ("id", "app_id"):
                continue
            list_display.append(field.name)
        return list_display

    display_id.short_description = "您的应用唯一ID"
