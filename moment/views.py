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

    @action(detail=False, methods=['get'])
    def lasted(self, request):
        moments = Moment.objects.latest('moment_id')
        moments_ser = self.get_serializer(moments)
        return Response(moments_ser.data, status=status.HTTP_400_BAD_REQUEST)
