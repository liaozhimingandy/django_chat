#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""=================================================
    @Project: settings.py
    @File： api.py
    @Author：liaozhimingandy
    @Email: liaozhimingandy@gmail.com
    @Date：2024-04-12 10:20
================================================="""
import uuid
from datetime import timedelta
from typing import Optional

from ninja import Router, Schema

from oauth.authentication import AuthBearer
from oauth.common.token import generate_jwt_token
from oauth.models import App

router = Router(tags=["oauth"])


class AccessTokenSchema(Schema):
    access_token: str
    expires_in: int
    token_type: str = 'bearer'
    scop: str
    app_id: Optional[str] = None


class RefreshTokenSchema(AccessTokenSchema):
    refresh_token: Optional[str] = None


class Error(Schema):
    message: str


@router.get("/authorize/{app_id}/{app_secret}/{grant_type}/", auth=None, response={200: RefreshTokenSchema, 403: Error})
def authorize(request, app_id: str, app_secret: str, grant_type: str):
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
        return 403, {"message": str(e)}
    except App.DoesNotExist:
        return 403, {"message": "No Found"}

    # 作废之前的salt
    app.salt = str(uuid.uuid4()).replace('-', '')[:8]
    app.save()
    data = {"app_id": str(app_id), "salt": app.salt}

    token_refresh = generate_jwt_token(data, expires_in=timedelta(days=30))
    token_access = generate_jwt_token(data, grant_type="access_token")
    token_access.update({"refresh_token": token_refresh.get("access_token"), "app_id": str(app_id)})

    return 200, token_access


@router.get("/refresh-token/{app_id}/{grant_type}/", response={200: AccessTokenSchema, 403: Error})
def refresh_token(request, app_id: str, grant_type: str):
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
        return 403, {"message": str(e)}
    try:
        app = App.objects.get(app_id=app_id, is_active=True)
        assert request.user.username == app.salt, "app_secret changed, please login again!"
    except App.DoesNotExist:
        return 403, {"message": "No Found"}
    except AssertionError as e:
        return 403, {"message": str(e)}

    data = {"app_id": str(app_id), "salt": app.salt}

    # 生成请求令牌
    token_access = generate_jwt_token(data, grant_type="access_token")
    token_access.update({"app_id": str(app_id)})

    return 200, token_access


@router.get("test-oauth/")
def test_oauth(request):
    return 200, {"message": "hello word"}


if __name__ == "__main__":
    pass
