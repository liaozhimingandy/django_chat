"""django_welink URL Configuration

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
from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.conf import settings

from moment import urls as moment_urls
from user import urls as user_urls

from user.views import OauthESBViewSet, OauthViewSet

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    re_path('^api/moment/', include((moment_urls, 'moment'), namespace='moment')),
    re_path('^api/user/', include((user_urls, 'user'), namespace='user')),
    re_path('^api/esb/oauth/authorize/', OauthESBViewSet.as_view({"get": "authorize"}), name="authorize"),  # 临时使用
    re_path('^api/esb/oauth/refresh-token/', OauthESBViewSet.as_view({"get": "authorize"}), name="refresh-token"),
    # 临时使用
    path('api/oauth/authorize/<str:client_id>/<str:client_secret>/<str:username>/<str:password>/<str:grant_type>/',
         OauthViewSet.as_view({"get": "authorize"}), name="authorize-v2"),  # 临时使用
    path('api/oauth/refresh-token/<str:client_id>/<str:client_secret>/<str:grant_type>/',
         OauthViewSet.as_view({"get": "refresh_token"}), name="refresh-token-v2"),  # 临时使用
]

# 拼接文件查看路径,用于查看图片
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
