from django.contrib import admin

from comment.models import Comment


# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', "account", "content", "post", "is_root")
    list_per_page = 10
