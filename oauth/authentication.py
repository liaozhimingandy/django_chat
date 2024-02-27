from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed

from oauth.common.token import verify_jwt_token


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):

        authorization = request.META.get('HTTP_AUTHORIZATION', '')  # 从请求头获取token

        if not authorization:
            raise AuthenticationFailed({"message": "please use a token to request"})

        # 校验jwt token并解析数据
        jwt_decode = verify_jwt_token(authorization.split()[1], grant_type= "client_credential"
        if request.resolver_match.view_name == "oauth:refresh_token" else "access_token")

        if len(jwt_decode.keys()) < 2:
            raise AuthenticationFailed(jwt_decode)

        # 判断如果不是请求刷新令牌请求,则需使用access_token进行发起请求
        if request.resolver_match.view_name != "oauth:refresh_token" and jwt_decode.get("grant_type") != "access_token":
            raise AuthenticationFailed({"message": "please use access_token!"})

        # 借用user保存登录信息
        user = User(id=jwt_decode['app_id'], username=jwt_decode['salt'])

        return user, None