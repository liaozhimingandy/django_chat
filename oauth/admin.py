from django.contrib import admin

from oauth.models import App


# Register your models here.
@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = [field.name for field in App._meta.fields]