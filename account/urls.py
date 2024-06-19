# url 命令空间
from rest_framework.routers import DefaultRouter

from .views import AccountViewSet, OauthViewSet

app_name = 'account'

urlpatterns = []
# api根路由
router = DefaultRouter()
router.register('account', AccountViewSet, basename='account')
router.register('oauth', OauthViewSet, basename='oauth')
urlpatterns += router.urls

