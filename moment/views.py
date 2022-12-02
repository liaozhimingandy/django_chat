import datetime

import pytz
from rest_framework.decorators import action
from rest_framework.response import Response

from moment.models import Moment
from rest_framework import viewsets, status
from moment.serializers import MomentSerializer


# Create your views here.
class MomentViewSet(viewsets.ModelViewSet):
    """
    动态视图集
    """
    queryset = Moment.objects.all()
    serializer_class = MomentSerializer

    def list(self, request):
        qs = Moment.objects.all()
        moments = MomentSerializer(qs, many=True)

        return Response(moments.data)

    def create(self, request):
        moment = request.data

        ip = request.META.get('HTTP_X_FORWARDED_FOR') if 'HTTP_X_FORWARDED_FOR' in request.META \
            else request.META.get('REMOTE_ADDR')
        moment["from_ip"] = ip

        serializer = MomentSerializer(data=moment)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = {
            "code": 200,
            "msg": "保存成功",
            "gmt_created": datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai')).isoformat(sep='T', timespec='seconds')
        }
        return Response(data=data)

    @action(detail=False, methods=['get'])
    def lasted(self, request):
        """返回最近十条数据"""
        moments = Moment.objects.order_by('-moment_id')[:10]
        moments_ser = self.get_serializer(moments, many=True)

        data = {
            "code": 200,
            "msg": "处理成功",
            "gmt_created": datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai')).isoformat(sep='T',
                                                                                              timespec='seconds'),
            "data": moments_ser.data
        }
        return Response(data, status=status.HTTP_200_OK)
