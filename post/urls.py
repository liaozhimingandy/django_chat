# url 命令空间
from rest_framework.routers import DefaultRouter

from post import views

app_name = 'post'

urlpatterns = []
# api根路由
router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='post')
router.register(r'likes', views.LikeViewSet, basename='like')
router.register(r'comments', views.CommentViewSet, basename='comment')
router.register(r'upload', views.UploadViewSet, basename='upload')
urlpatterns += router.urls

