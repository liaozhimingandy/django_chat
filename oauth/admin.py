from django.contrib import admin
from django.conf import settings

from oauth.models import App


# Register your models here.
@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display_links = ["display_app_id", ]
    # list_display = [field.name for field in App._meta.fields]
    readonly_fields = ["display_app_id", ]

    def display_app_id(self, obj):
        return f"{settings.PREFIX_ID}{obj.app_id}"

    def get_list_display(self, request):
        """返回要显示的字段列表"""
        list_display = ["display_app_id", ]
        for field in App._meta.fields:
            if field.name in ("app_id", "id"):
                continue
            list_display.append(field.name)
        return list_display

    display_app_id.short_description = "您的应用唯一ID"
