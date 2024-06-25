from django.contrib import admin

from django_chat import settings
from post.models import Post, Image, Comment, Like


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'account_id', 'content', 'gmt_created']
    exclude = ['gmt_created', ]
    # 搜索
    search_fields = ['account_id']
    # 分页 - 设置每页最大显示数目
    list_per_page = 10


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ["id", 'image_name', "image_md5", 'gmt_created']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', "account_id", "content", "post_id", "is_root")
    list_per_page = 10

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Like._meta.fields]
    list_per_page = 10