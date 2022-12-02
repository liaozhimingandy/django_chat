from rest_framework import serializers
from moment.models import Moment


class MomentSerializer(serializers.ModelSerializer):
    # 补充数据库不存在的字段
    user_name = serializers.SerializerMethodField(label='用户昵称')

    class Meta:
        model = Moment
        # fields = '__all__'
        # exclude = ['poi', '']
        fields = ['user_name', ] + [item.name for item in Moment._meta.fields]

    def get_user_name(self, obj):
        # game_name = models.Games.objects.get(uuid=obj.game_uuid).name
        user_name = '匿名用户'
        return user_name
