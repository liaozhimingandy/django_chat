from rest_framework.decorators import action
from rest_framework.response import Response

from moment.models import Moment
from rest_framework import viewsets, status
from moment.serializers import MomentSerializer


# Create your views here.
class MomentViewSet(viewsets.ViewSet):
    """
    动态视图集
    """

    def list(self, request):
        qs = Moment.objects.all()
        moments = MomentSerializer(qs, many=True)

        return Response(moments.data)

    def create(self, request):
        print(request.data)
        r = Response({'gmt_created': 1})
        r['Access-Control-Allow-Origin'] = '*'
        r['Access-Control-Allow-Methods'] = 'post'
        r['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
        return Response({'gmt_created': 1})

    @action(detail=False, methods=['get'])
    def lasted(self, request):
        """返回最近十条数据"""
        moments = Moment.objects.order_by('-moment_id')[:10]
        moments_ser = self.get_serializer(moments, many=True)
        return Response(moments_ser.data, status=status.HTTP_400_BAD_REQUEST)
