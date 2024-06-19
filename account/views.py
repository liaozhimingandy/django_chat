import uuid
from datetime import timedelta

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.conf import settings

from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.decorators import action, api_view

from account.authentication import JWTAuthBearer
from account.common.token import generate_jwt_token
from account.models import Account, App
from account.serializers import AccountSerializer


# Create your views here.
class AccountViewSet(ViewSet):

    def list(self, request):
        return Response(data="Hello World")

    @action(detail=False, methods=["POST"], url_path="register")
    def create_account(self, request):
        """
        用户注册
        :param request:
        :return:
        """
        payload = request.data
        serializer = AccountSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["POST"], url_path="password/change")
    def password_change(self, request):
        """
        密码修改
        :param request:
        :return:
        """
        payload = request.data
        account = get_object_or_404(Account, username=payload["username"],
                                    password=payload["current_password"])
        account.password = payload["password"]
        account.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["POST"], url_path="password/reset")
    def password_reset(self, request):
        """
        密码重置
        :param request:
        :return:
        """
        payload = request.data
        account = get_object_or_404(Account, username=payload["username"])
        account.password = payload["password"]
        account.save()
        serializer = AccountSerializer(account)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"], url_path="(?P<username>\w+)")
    def get_account(self, request, username: str = None):
        """
        获取用户信息
        :param request:
        :param username:
        :return:
        """
        account = get_object_or_404(Account, username=username)
        serializer = AccountSerializer(account)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["PUT"], url_path="(?P<username>\w+)/info")
    def update_account(self, request, username: str = None):
        """
        更新用户信息
        :param request:
        :param username:
        :return:
        """
        payload = request.data
        account = get_object_or_404(Account, username=username)
        for attr, value in payload.items():
            setattr(account, attr, value)
        account.save()
        serializer = AccountSerializer(account)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"], url_path="search/(?P<keyword>\w+)")
    def account_search(self, request, keyword: str):
        """账户查询"""
        accounts = Account.objects.filter(Q(username__icontains=keyword) | Q(nick_name__icontains=keyword))
        serializer = AccountSerializer(accounts, many=True)
        return Response(data=serializer.data)


class OauthViewSet(ViewSet):
    """
    认证下相关
    """

    def list(self, request):
        return Response(data={"message": "oauth"})

    @action(detail=False, methods=["GET"], url_path="authorize/(?P<app_id>\w+)/(?P<app_secret>\w+)/(?P<grant_type>\w+)")
    def authorize(self, request, app_id: str, app_secret: str, grant_type: str = "client_credential"):
        """
         用户进行认证获取刷新令牌
        :param request:
        :param app_id:
        :param app_secret:
        :param grant_type:
        :return:
        """
        try:
            assert len(app_secret) > 0, "app_secret must exists"
            assert grant_type == "client_credential", "grant_type must equal client_credential"
            app = App.objects.get(app_id=app_id.replace(settings.PREFIX_ID, ''), app_secret=app_secret, is_active=True)
        except AssertionError as e:
            return Response(data={"message": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except App.DoesNotExist:
            return Response({"message": "No Found"}, status=status.HTTP_403_FORBIDDEN)

        # 作废之前的salt
        app.salt = uuid.uuid4().hex[:8]
        app.save()
        data = {"app_id": str(app_id), "salt": app.salt}

        token_refresh = generate_jwt_token(data, expires_in=timedelta(days=7), grant_type=grant_type)
        token_refresh.update(**{"app_id": app_id, "refresh_token": token_refresh.get("access_token", None)})
        token_refresh.pop("access_token", None)

        return Response(data=token_refresh, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"], url_path="refresh-token/(?P<app_id>\w+)/(?P<grant_type>\w+)",
            authentication_classes=[JWTAuthBearer, ])
    def refresh_token(self, request, app_id: str, grant_type: str = "refresh_token"):
        """
        使用刷新令牌进行更新获取权限令牌,请使用postman测试,header携带认证信息,后续会实现,refresh_token有效期为7天,请妥善保管,重新登录认证后,
        该token作废;
        :param request:
        :param app_id:
        :param grant_type:
        :return:
        """
        try:
            assert grant_type == "refresh_token", "grant_type must equal refresh_token"
        except AssertionError as e:
            return Response({"message": str(e)}, status=status.HTTP_403_FORBIDDEN)

        try:
            app = App.objects.get(app_id=app_id.replace(settings.PREFIX_ID, ''), is_active=True)
            assert request.user.username == app.salt, "app_secret or salt changed, please login again!"
        except App.DoesNotExist:
            return Response({"message": "No Found"}, status=status.HTTP_403_FORBIDDEN)
        except AssertionError as e:
            return Response({"message": str(e)}, status=status.HTTP_403_FORBIDDEN)

        data = {"app_id": app_id, "salt": app.salt, "jwt_app_id": app_id}
        token_access = generate_jwt_token(data, grant_type="access_token", expires_in=timedelta(hours=2))

        return Response(data=token_access, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"], url_path="test-oauth", authentication_classes=[JWTAuthBearer, ])
    def test_oauth(self, request):
        """测试接口"""
        return Response({"message": "hello word"})
