from django.contrib.auth.models import User
from ninja.errors import AuthenticationError
from ninja.security import HttpBearer

from oauth.common.token import verify_jwt_token


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        if not token:
            raise AuthenticationError({"message": "please use a token to request"})

        # 校验jwt token并解析数据
        grant_type = "client_credential" if request.resolver_match.view_name == "api-1.0.0:refresh_token" \
            else "access_token"
        jwt_decode = verify_jwt_token(token, grant_type=grant_type)

        if len(jwt_decode.keys()) < 2:
            raise AuthenticationError(jwt_decode)

        # 判断如果不是请求刷新令牌请求,则需使用access_token进行发起请求
        if (request.resolver_match.view_name != "api-1.0.0:refresh_token"
                and jwt_decode.get("grant_type") != "access_token"):
            raise AuthenticationError({"message": "please use access_token to request!"})

        # 借用user保存登录信息
        user = User(id=jwt_decode['app_id'], username=jwt_decode['salt'])

        request.user = user

        return user
