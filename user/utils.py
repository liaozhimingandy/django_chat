import datetime
import os
import uuid

import jwt
from user.models import User
from jwt.exceptions import ExpiredSignatureError
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class Singleton(object):
    def __init__(self, cls):
        self._cls = cls
        self.uniqueInstance = None

    def __call__(self,  *args, **kwargs):
        if self.uniqueInstance is None:
            self.uniqueInstance = self._cls(*args, **kwargs)
        return self.uniqueInstance


class TokenUtils:
    """token工具类,用于生成token以及校验"""
    # 默认头部
    header = {
        "alg": "HS256",
        "typ": "JWT"
    }

    # 盐, 取setting中的密钥
    salt = os.getenv("SECRET_KEY", "django-insecure-^xs70#xch%!em*b#%)jp!$&69m=ttoek&6_@cm-sgj%7ia!r80")

    @classmethod
    def create_token(cls, payload, token_timeout=7200, refresh_timeout=30):
        """创建token"""
        # 盐salt
        # 业务数据 payload
        # iss: 该JWT的签发者，是否使用是可选的；
        # sub: 该JWT所面向的用户，是否使用是可选的；
        # aud: 接收该JWT的一方，是否使用是可选的；
        # exp(expires): 什么时候过期，这里是一个Unix时间戳，是否使用是可选的；
        # iat(issued
        # at): 在什么时候签发的(UNIX时间)，是否使用是可选的
        # jti: jwt的唯一身份标识，主要用来作为一次性token，从而回避重放攻击
        # nbf (Not Before)：它指的是该 token 的生效时间，如果使用但是没到生效时间则抛出
        # grant_type 类型
        # 授权码模式（grant_type - -->authorization_code）
        # 简化模式（response_type - -->token）
        # 密码模式（grant_type - -->password）
        # 客户端模式（grant_type - -->client_credentials）
        # 授权码模式：安全性高，使用率高，流程复杂。要求第三方应用必须有服务器。对安全性要求较高，web项目中一般使用授权码模式。
        # 简化模式：流程简单；适用于纯前端应用，不安全。Token有效期短，浏览器关闭即失效
        # 密码模式：需要输入账号密码，极度不安全，需要高度信任第三方应用适用于其他授权模式都无法采用的情况；原生APP可以使用，web不建议使用
        # 客户端模式：授权维度为应用维度，而不是用户维度。因此有可能多个用户共用一个Token的情况。适用于应用维度的共享资源。适用于服务器之间交互，不需要用户参与。
        payload["aud"] = "www.alsoapp.com"
        payload["iss"] = "Online JWT Builder"
        payload["jti"] = str(uuid.uuid4()).replace('-', '')
        payload['iat'] = int(datetime.datetime.now().timestamp())
        payload['nbf'] = payload['iat']
        payload['exp'] = int((datetime.datetime.now() + datetime.timedelta(minutes=token_timeout)).timestamp())
        payload['grant_type'] = 'client_credential'

        # 默认不可逆加密算法为HS256
        token = jwt.encode(headers=cls.header, payload=payload, key=cls.salt, algorithm='HS256')

        # 得到refesh
        payload['exp'] = int((datetime.datetime.utcnow() + datetime.timedelta(days=refresh_timeout)).timestamp())
        payload['grant_type'] = 'refresh_token'
        refresh = jwt.encode(headers=cls.header, payload=payload, key=cls.salt)
        return {"access_token": token, "refresh_token": refresh, "expires_in": token_timeout, "token_type": "bearer",
                "scop": "read"}

    @classmethod
    def authenticate_token(cls, access_token):
        """校验token"""
        # 解码token
        try:
            payload = jwt.decode(jwt=access_token, key=cls.salt, audience='www.alsoapp.com', verify=True,
                                 algorithms=['HS256'])
        except ExpiredSignatureError:
            raise AuthenticationFailed('Token expired ')
        except jwt.DecodeError:
            raise AuthenticationFailed('Token authentication failed')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        return True, payload

    @classmethod
    def authenticate_refresh_token(cls, refresh_token):
        """校验refresh"""
        payload = cls.authenticate_token(access_token=refresh_token)[1]

        # 校验token 是否有效，以及是否是refresh token，验证通过后生成新的token 以及 refresh_token
        if payload and payload.get('grant_type') == 'refresh_token':
            # 如果需要标记此token 已经使用，需要借助redis 或者数据库（推荐redis）
            return True, payload
        else:
            raise AuthenticationFailed('Not a refresh_token')

    @classmethod
    def authenticate_access_token(cls, access_token):
        """校验refresh"""
        payload = cls.authenticate_token(access_token=access_token)[1]

        # 校验token 是否有效，以及是否是refresh token，验证通过后生成新的token 以及 refresh_token
        if payload and payload.get('grant_type') == 'client_credential':
            # 如果需要标记此token 已经使用，需要借助redis 或者数据库（推荐redis）
            return True, payload
        else:
            raise AuthenticationFailed('Not a access_token')


class JWTAuthentication(BaseAuthentication):
    """
    JWT认证;
    参考文档:# https://www.cnblogs.com/gcxblogs/p/13376058.html
    """

    def authenticate(self, request):
        authorization = request.META.get('HTTP_AUTHORIZATION', None)
        if not authorization:
            raise AuthenticationFailed({'msg': '未获取到Authorization请求头', "code": 403})
        access_token = authorization.split(' ')
        if access_token[0].lower() != 'bearer':
            raise AuthenticationFailed({'msg': 'Authorization请求头中认证方式错误', "code": 403})

        # 校验token
        payload = TokenUtils.authenticate_access_token(access_token=access_token[1])

        # 从用户表获取用户
        user = User.objects.filter(id=payload[1].get('uid', None)).first()
        return user, None
