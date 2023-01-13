from rest_framework.routers import DefaultRouter

from user.views import OauthViewSet

# urlpatterns = [
#     # re_path('^oauth/authorize/', OauthViewSet.as_view({"get": "authorize"})),
# ]

# url 命令空间
app_name = 'user'

# api根路由
router = DefaultRouter()
router.register('oauth', OauthViewSet, basename="oauth")  # 向路由器中注册视图集,"user":浏览器访问的路径，basename:路由别名

urlpatterns = router.urls
