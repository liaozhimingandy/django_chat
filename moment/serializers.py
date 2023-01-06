from rest_framework import serializers
from moment.models import Moment
from user.models import User


class MomentSerializer(serializers.ModelSerializer):
    # 补充数据库不存在的字段
    nick_name = serializers.SerializerMethodField(label='用户昵称')
    username = serializers.SerializerMethodField(label='用户名称', method_name='get_username')

    class Meta:
        model = Moment
        # fields = '__all__'
        # exclude = ['poi', '']
        fields = ['nick_name', 'username'] + [item.name for item in Moment._meta.fields]

    def get_nick_name(self, obj):
        # game_name = models.Games.objects.get(uuid=obj.game_uuid).name
        return User.objects.get(uid=obj.uid).nick_name

    def get_username(self, obj):
        return User.objects.get(uid=obj.uid).username


class ImageUploadSerializer(serializers.Serializer):
    """
    图片上传
    """
    image = serializers.ImageField(label="图片", max_length=128, use_url=True, error_messages={
            'invalid': '图片参数错误'
        })

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

