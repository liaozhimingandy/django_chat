"""dj_api_luohu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import re_path
from rest_framework.routers import DefaultRouter

from user.views import OauthViewSet

# urlpatterns = [
#     # re_path('^oauth/authorize/', OauthViewSet.as_view({"get": "authorize"})),
# ]

# api根路由
router = DefaultRouter()
router.register('oauth', OauthViewSet, basename="oauth")  # 向路由器中注册视图集,"user":浏览器访问的路径，basename:路由别名

urlpatterns = router.urls