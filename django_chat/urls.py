"""django_chat URL Configuration

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
from django.conf.urls.static import static
from django.conf import settings

from post import urls as post_urls
from account import urls as account_urls

urlpatterns = [
    # django 后台相关路由
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls, name="admin"),
    # 账号相关路由
    re_path('^auth/', include(account_urls, namespace='auth')),
    # re_path('^oauth/', include((oauth_urls, 'oauth'), namespace='oauth')),
    # 帖子相关路由
    re_path('^v2/', include(post_urls, namespace='v2')),
    # drf 框架认证路由
    path('api-auth/', include('rest_framework.urls')),
]

# 开发环境提供静态文件和多媒体查看功能;这一般会在 DEBUG is set to True 情况下由 runserver 自动完成
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
