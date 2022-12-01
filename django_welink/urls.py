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
from django.urls import path
from rest_framework.routers import DefaultRouter
from moment.views import MomentViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
]

router = DefaultRouter()  # 可以处理视图的路由器
router.register('api/moments', MomentViewSet, basename="moment")  # 向路由器中注册视图集,"user":浏览器访问的路径，basename:路由别名
# router.register('DemoAPIView', DemoAPIView, basename="demo")
urlpatterns += router.urls  # 将路由器中的所以路由信息追到到django的路由列表中
