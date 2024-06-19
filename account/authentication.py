from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed

from .common.token import verify_jwt_token


class JWTAuthBearer(authentication.BaseAuthentication):
    """Bearer authentication
    todo: 后续完善错误详细,目前统一返回 "detail": "Unauthorized"
    """

    def authenticate(self, request):

        token = request.META.get('HTTP_AUTHORIZATION', '')  # 从请求头获取token

        if not token:
            raise AuthenticationFailed({"message": "please use a token to request"})

        jwt_decode = verify_jwt_token(token.split()[1], grant_type="client_credential"
        if request.resolver_match.view_name == "auth:oauth-refresh-token" else "access_token")

        # 如果验证成功,则返回多个key的数据
        if len(jwt_decode.keys()) < 2:
            raise AuthenticationFailed(jwt_decode)

        # 判断如果不是请求刷新令牌请求,则需使用access_token进行发起请求
        if request.resolver_match.view_name != "auth:oauth-refresh-token" and jwt_decode.get(
                "grant_type") != "access_token":
            raise AuthenticationFailed({"message": "please use access_token!"})

        # 借用user保存登录信息
        user = User(id=jwt_decode['app_id'], username=jwt_decode['salt'])

        return user, None
