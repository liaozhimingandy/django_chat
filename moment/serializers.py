from rest_framework import serializers
from moment.models import Moment


class MomentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moment
        fields = '__all__'
