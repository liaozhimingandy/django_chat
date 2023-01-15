from django.urls import path
from rest_framework.routers import DefaultRouter

from user.views import OauthViewSet
# url 命令空间
app_name = 'user'
# urlpatterns = [
#     path('oauth/authorize/<str:client_id>/<str:client_secret>/<str:username>/<str:password>/<str'
#          ':grant_type>/', OauthViewSet.as_view({"get": "authorize"})),
# ]

# api根路由
router = DefaultRouter()
router.register('oauth', OauthViewSet, basename="oauth")  # 向路由器中注册视图集,"user":浏览器访问的路径，basename:路由别名

urlpatterns = router.urls
