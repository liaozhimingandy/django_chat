import uuid
from datetime import timedelta
from uuid import UUID

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, throttle_classes
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle, AnonRateThrottle, UserRateThrottle
from rest_framework.views import APIView

from oauth.authentication import JWTAuthentication
from oauth.common.token import generate_jwt_token
from oauth.models import App


# Create your views here.
# @extend_schema(summary="登录认证", tags=["oauth"], responses={200: AuthorizeTokenSerializer})
@api_view(http_method_names=['GET'])
@throttle_classes([AnonRateThrottle])
def authorize(request, app_id: UUID, app_secret: str, grant_type: str = "client_credential"):
    """

    用户进行认证获取刷新令牌

    :param request:<br>
    :param app_id: 应用唯一标识 <br>
    :param app_secret: 应用密钥 <br>
    :param grant_type: 固定值: client_credential <br>
    :return: 令牌信息或报错信息
    """

    try:
        assert len(app_secret) > 0, "app_secret must exists"
        assert grant_type == "client_credential", "grant_type must equal client_credential"
        app = App.objects.get(app_id=app_id, app_secret=app_secret, is_active=True)
    except AssertionError as e:
        return Response(data={"message": str(e)}, status=status.HTTP_403_FORBIDDEN)
    except App.DoesNotExist:
        return Response({"message": "No Found"}, status=status.HTTP_403_FORBIDDEN)

    # 作废之前的salt
    app.salt = str(uuid.uuid4()).replace('-', '')[:8]
    app.save()
    data = {"app_id": str(app_id), "salt": app.salt}

    token_refresh = generate_jwt_token(data, expires_in=timedelta(days=30))
    token_access = generate_jwt_token(data, grant_type="access_token")
    token_access.update({"refresh_token": token_refresh.get("access_token"), "app_id": str(app_id)})

    return Response(data=token_access, status=status.HTTP_200_OK)


class AuthorizeView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "oauth_authorize"

    def get(self, request, app_id: UUID, app_secret: str, grant_type: str = "client_credential", format=None):
        """

        用户使用平台分配的用户系统唯一标识和密钥进行认证获取刷新令牌,同时返回一个请求令牌

        :param request:<br>
        :param app_id: 应用唯一标识 <br>
        :param app_secret: 应用密钥 <br>
        :param grant_type: 固定值: client_credential <br>
        :return: 令牌信息或报错信息
        """
        throttle_scope = 'oauth_authorize'
        try:
            assert len(app_secret) > 0, "app_secret must exists"
            assert grant_type == "client_credential", "grant_type must equal client_credential"
            app = App.objects.get(app_id=app_id, app_secret=app_secret, is_active=True)
        except AssertionError as e:
            return Response(data={"message": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except App.DoesNotExist:
            return Response({"message": "No Found"}, status=status.HTTP_403_FORBIDDEN)

        # 作废之前的salt
        app.salt = str(uuid.uuid4()).replace('-', '')[:8]
        app.save()
        data = {"app_id": str(app_id), "salt": app.salt}

        # 生成一个刷新令牌
        token_refresh = generate_jwt_token(data, expires_in=timedelta(days=7))

        # 生成一个请求令牌
        token_access = generate_jwt_token(data, grant_type="access_token")
        token_access.update({"refresh_token": token_refresh.get("access_token"), "app_id": str(app_id)})

        return Response(data=token_access, status=status.HTTP_200_OK)


# @extend_schema(summary="获取权限令牌", tags=["oauth"], responses={200: RefreshTokenSerializer})
@api_view(http_method_names=['GET'])
@throttle_classes([ScopedRateThrottle])
@authentication_classes([JWTAuthentication])
def refresh_token(request, app_id: UUID, grant_type: str = "refresh_token"):
    """

     使用刷新令牌进行更新获取权限令牌,请使用postman测试,header携带认证信息,后续会实现,refresh_token有效期为30天,请妥善保管,重新登录认证后,
     该token作废;

    :param request: 请求对象<br>
    :param authorization: Bearer 您的refresh_token <br>
    :param app_id: 应用唯一标识 <br>
    :param grant_type: 固定值: refresh_token <br>
    :return:
    """
    # authorization = request.META.get('HTTP_AUTHORIZATION', '').split()[1] # 从请求头获取token
    # 使用JWT认证模块进行认证,借用user对象存储相关信息

    try:
        assert grant_type == "refresh_token", "grant_type must equal refresh_token"

    except AssertionError as e:
        return Response({"message": str(e)}, status=status.HTTP_403_FORBIDDEN)

    try:
        app = App.objects.get(app_id=app_id, is_active=True)
        assert request.user.username == app.salt, "app_secret changed, please login again!"
    except App.DoesNotExist:
        return Response({"message": "No Found"}, status=status.HTTP_403_FORBIDDEN)
    except AssertionError as e:
        return Response({"message": str(e)}, status=status.HTTP_403_FORBIDDEN)

    data = {"uid": str(app_id), "salt": app.salt}

    # 生成请求令牌
    token_access = generate_jwt_token(data, grant_type="access_token")

    return Response(data=token_access, status=status.HTTP_200_OK)


class TokenRefreshView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "oauth_refresh_token"
    authentication_classes = [JWTAuthentication]

    def get(self, request, app_id: UUID, grant_type: str = "refresh_token", format=None):
        """

        使用刷新令牌进行更新请求令牌,请使用postman测试,header携带认证信息,**refresh_token有效期为7天**,请妥善保管,重新登录认证后,
        该token作废;

        :param request: 请求对象<br>
        :param authorization: Bearer 您的refresh_token <br>
        :param app_id: 应用唯一标识 <br>
        :param grant_type: 固定值: refresh_token <br>
        :return:
        """
        # authorization = request.META.get('HTTP_AUTHORIZATION', '').split()[1] # 从请求头获取token
        # 使用JWT认证模块进行认证,借用user对象存储相关信息

        try:
            assert grant_type == "refresh_token", "grant_type must equal refresh_token"

        except AssertionError as e:
            return Response({"message": str(e)}, status=status.HTTP_403_FORBIDDEN)

        try:
            app = App.objects.get(app_id=app_id, is_active=True)
            assert request.user.username == app.salt, "app_secret changed, please login again!"
        except App.DoesNotExist:
            return Response({"message": "No Found"}, status=status.HTTP_403_FORBIDDEN)
        except AssertionError as e:
            return Response({"message": str(e)}, status=status.HTTP_403_FORBIDDEN)

        data = {"uid": str(app_id), "salt": app.salt}

        # 生成一个请求令牌
        token_access = generate_jwt_token(data, grant_type="access_token")

        return Response(data=token_access, status=status.HTTP_200_OK)


class TestOauthView(APIView):
    """测试接口"""

    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    # authentication_classes = [JWTAuthentication]

    def get(self, request):
        return Response(data={"message": "hello word"}, status=status.HTTP_200_OK)
