from django.contrib import admin

from comment.models import Comment


# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', "account_id", "content", "post_id", "is_root")
    list_per_page = 10
