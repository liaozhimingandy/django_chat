from rest_framework.routers import DefaultRouter

from moment.views import MomentViewSet, ImageViewSet

# url 命令空间
app_name = 'moment'

urlpatterns = [

]

# api根路由
router = DefaultRouter()
router.register('moments', MomentViewSet, basename="moment")  # 向路由器中注册视图集,"user":浏览器访问的路径，basename:路由别名
router.register('image', ImageViewSet, basename="upload_images")

urlpatterns += router.urls
