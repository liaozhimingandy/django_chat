from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from moment.models import Moment
from rest_framework import viewsets, status
from moment.serializers import MomentSerializer

from user.lib.TokenUtil import JWTAuthentication

# Create your views here.
class MomentViewSet(viewsets.ModelViewSet):
    """
    动态视图集
    """
    queryset = Moment.objects.filter(right_status=0).order_by('-moment_id').all()
    serializer_class = MomentSerializer

    # 限流设置
    throttle_classes = (AnonRateThrottle,)

    # 使用过滤器, 指定哪个可过滤
    filter_fields = ['user_name', 'mobile']

    # 指定后端排序
    filter_backends = [OrderingFilter, ]
    # 排序设置
    ordering_fields = ['moment_id', 'user_name']

    # 权限设置
    # IsAuthenticated: 只有登录才能访问
    # IsAuthenticatedOrReadOnly: 认证用户可读可写，未认证用户可读
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    # 通过Authorization请求头传递token
    authentication_classes = [JWTAuthentication, ]

    def create(self, request, *args, **kwargs):
        moment = request.data

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
        moments = Moment.objects.order_by('-moment_id')[:10]
        moments_ser = self.get_serializer(moments, many=True)

        # data = {
        #     "code": 200,
        #     "msg": "处理成功",
        #     "gmt_created": datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai')).isoformat(sep='T',
        #                                                                                       timespec='seconds'),
        #     "data": moments_ser.data
        # }
        return Response(moments_ser.data, status=status.HTTP_200_OK)
