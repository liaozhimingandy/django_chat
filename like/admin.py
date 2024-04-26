from django.contrib import admin

from like.models import Like


# Register your models here.

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Like._meta.fields]
    list_per_page = 10
