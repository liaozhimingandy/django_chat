import uuid

from rest_framework import serializers


class RefreshTokenSerializer(serializers.Serializer):
    """刷新令牌"""
    access_token = serializers.CharField()
    expires_in = serializers.IntegerField(default=7200)
    token_type = serializers.CharField(default='bearer')
    scope = serializers.CharField(default='all')
    app_id = serializers.CharField(default=uuid.uuid4())

class AuthorizeTokenSerializer(RefreshTokenSerializer):
    """认证时返回令牌信息"""
    refresh_token = serializers.CharField()
