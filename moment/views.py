from copy import deepcopy

from django.http import QueryDict
from django.urls import reverse
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import action, api_view
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from django_welink import settings
from moment.lib import utils
from moment.lib.utils import get_uploaded_file_md5
from moment.models import Moment, Image
from rest_framework import viewsets, status
from moment.serializers import MomentSerializer, ImageUploadSerializer


# Create your views here.
class MomentViewSet(viewsets.ModelViewSet):
    """
    动态相关接口
    """
    queryset = Moment.objects.filter(right_status=0).order_by('-id').all()
    serializer_class = MomentSerializer

    # 限流设置
    throttle_classes = (UserRateThrottle, AnonRateThrottle)

    # 通过Authorization请求头传递token
    # authentication_classes = [BasicAuthentication, ]
    # 权限设置
    # IsAuthenticated: 只有登录才能访问
    # IsAuthenticatedOrReadOnly: 认证用户可读可写，未认证用户可读
    # permission_classes = [IsAuthenticatedOrReadOnly, ]

    def create(self, request, *args, **kwargs):
        moment = request.data
        moment_dict = moment.copy()

        # 提取请求ip地址
        ip = request.META.get('HTTP_X_FORWARDED_FOR') if 'HTTP_X_FORWARDED_FOR' in request.META \
            else request.META.get('REMOTE_ADDR')
        moment_dict.update({'from_ip': ip})

        serializer = self.get_serializer(data=moment_dict)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['get'])
    def lasted(self, request):
        """返回最近十条数据"""
        moments = Moment.objects.order_by('-id')[:10]
        moments_ser = self.get_serializer(moments, many=True)

        return Response(moments_ser.data, status=status.HTTP_200_OK)


class ImageViewSet(viewsets.GenericViewSet):

    serializer_class = ImageUploadSerializer

    @action(detail=False, methods=['post'], url_path="upload")
    def upload(self, request):
        """
        图片上传接口
        :param request: 图片路径
        :return:
        """
        data = request.data

        # 获取图片md5
        image_copy = deepcopy(data['image'])
        image_md5 = get_uploaded_file_md5(image_copy)
        del image_copy

        items = list(Image.objects.filter(image_md5=image_md5))
        if items:
            serializer = self.get_serializer(items[0])
            return Response(status=status.HTTP_200_OK, data=serializer.data)

        try:
            data['image_md5'] = image_md5
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        # 未知错误，报服务器内部错误
        except (Exception, ) as error:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={"detail": str(error)})


@api_view(['GET'])
def test(request):
    data = {
        "test": reverse("moment:test"),
        "refresh-token": reverse("refresh-token"),
    }
    return Response(data=data, status=status.HTTP_200_OK)


