import json

from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from moment.lib import utils
from moment.models import Moment
from rest_framework import viewsets, status
from moment.serializers import MomentSerializer, ImageUploadSerializer

from user.lib.TokenUtil import JWTAuthentication


# Create your views here.
class MomentViewSet(viewsets.ModelViewSet):
    """
    动态视图集
    """
    queryset = Moment.objects.filter(right_status=0).order_by('-mid').all()
    serializer_class = MomentSerializer

    # 限流设置
    throttle_classes = (UserRateThrottle, AnonRateThrottle)

    # 使用过滤器, 指定哪个可过滤
    filter_fields = ['username', 'mobile']

    # 指定后端排序
    filter_backends = [OrderingFilter, ]
    # 排序设置
    ordering_fields = ['mid', 'username']

    # 权限设置
    # IsAuthenticated: 只有登录才能访问
    # IsAuthenticatedOrReadOnly: 认证用户可读可写，未认证用户可读
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    # 通过Authorization请求头传递token
    authentication_classes = [JWTAuthentication, ]

    def create(self, request, *args, **kwargs):
        moment = request.data

        # 提取请求ip地址
        ip = request.META.get('HTTP_X_FORWARDED_FOR') if 'HTTP_X_FORWARDED_FOR' in request.META \
            else request.META.get('REMOTE_ADDR')
        moment["from_ip"] = ip

        serializer = self.get_serializer(data=moment)
        serializer.is_valid(raise_exception=True)

        # data = {
        #     "code": 200,
        #     "msg": "保存成功",
        #     "gmt_created": datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai')).isoformat(sep='T', timespec='seconds')
        # }
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['get'])
    def lasted(self, request):
        """返回最近十条数据"""
        moments = Moment.objects.order_by('-mid')[:10]
        moments_ser = self.get_serializer(moments, many=True)

        # data = {
        #     "code": 200,
        #     "msg": "处理成功",
        #     "gmt_created": datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai')).isoformat(sep='T',
        #                                                                                       timespec='seconds'),
        #     "data": moments_ser.data
        # }
        return Response(moments_ser.data, status=status.HTTP_200_OK)


class ImageViewSet(viewsets.GenericViewSet):

    serializer_class = ImageUploadSerializer

    @action(detail=False, methods=['post'], url_path="upload")
    def upload(self, request, pk=None):
        """
        图片上传接口
        :param request: 图片路径
        :return:
        """
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            image = serializer.validated_data['image']
            img_file = "image"  # 图片存储的文件夹

            img_name = utils.save_img(image, img_file)
            img_url = utils.get_img_url(request, img_file, img_name)

            return Response(status=status.HTTP_201_CREATED, data=img_url)
        # 未知错误，报服务器内部错误
        except Exception as error:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={"detail": str(error)})


