from django.conf import settings

from rest_framework import serializers
from moment.models import Moment, Image


class MomentSerializer(serializers.ModelSerializer):
    # 补充数据库不存在的字段
    # nick_name = serializers.SerializerMethodField(label='用户昵称')
    # username = serializers.SerializerMethodField(label='用户名称', method_name='get_username')

    class Meta:
        model = Moment
        fields = '__all__'
        # exclude = ['from_ip', ]
        # fields = ['nick_name', 'username'] + [item.name for item in Moment._meta.fields]

    def to_representation(self, instance):
        """自定义返回之前处理逻辑"""
        data = super().to_representation(instance)
        if data['images']:
            new_images = [settings.MEDIA_DOMAIN_URL+item for item in data['images']]
            data['images'] = new_images
        # 补充额外字段
        # 采用此方式,避免多次查询数据库
        # user = User.objects.get(uid=instance.uid)
        # data['nick_name'] = user.nick_name
        # data['username'] = user.username
        return data


class ImageUploadSerializer(serializers.ModelSerializer):
    """
    图片上传接口
    """
    class Meta:
        model = Image
        fields = '__all__'



