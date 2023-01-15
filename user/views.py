import datetime
import time

from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, status

from user.lib.SQLServer import SQLServer
from user.lib.TokenUtil import TokenUtils

sql_exector = SQLServer(server=settings.TOKEN_DB_HOST, user=settings.TOKEN_DB_USER, password=settings.TOKEN_DB_PASSWORD,
                        database=settings.TOKEN_DB_NAME)


class OauthViewSet(viewsets.GenericViewSet):
    """
    示例: http://127.0.0.1:8000/api/v2/user/oauth/authorize/p2pweb/fgsdgrf/zhiming/123456/password/
    """

    @action(methods=('get',), detail=False, url_path=r'authorize/(?P<client_id>\w+)/(?P<client_secret>\w+)/('
                                                     r'?P<username>\w+)/(?P<password>\w+)/(?P<grant_type>\w+)',
            name='authorize')
    def authorize(self, request, username, password, grant_type, client_id=None, client_secret=None):
        """
        走密码方式授权获取token
        :param client_secret: 客户端秘钥
        :param client_id: 客户端接入标识
        :param grant_type: 授权类型
        :param password: 资源拥有者密码
        :param username: 资源拥有者用户名
        :param request:
        :return: token内容
        """
        # 判断授权方式
        if grant_type not in ('password', ):
            return Response(data={'code': 403, 'msg': '不支持的授权方式'}, status=status.HTTP_403_FORBIDDEN)
        # 验证密码
        user = authenticate(username=username, password=password)
        if user is None:
            return Response({'code': status.HTTP_401_UNAUTHORIZED, 'msg': '用户名或密码不正确!'}, status=status.HTTP_401_UNAUTHORIZED)

        payload = {"uid": user.uid,
                   'username': user.username}
        tokens = TokenUtils.create_token(payload=payload, token_timeout=7200*12)
        tokens['uid'] = user.uid
        tokens['nick_name'] = user.username

        return Response(tokens)

    @action(methods=('get',), detail=False, url_path=r"refresh-token/(?P<client_id>\w+)/(?P<client_secret>\w+)/("
                                                     r"?P<grant_type>\w+)", name='refresh-token')
    def refresh_token(self, request, grant_type, client_id=None, client_secret=None):
        """
        通过刷新令牌来更新请求token
        :param client_secret: 客户端秘钥
        :param client_id: 客户端接入标识
        :param grant_type: 授权类型
        :param request:
        :return: token内容
        """
        tokens = None
        # 判断授权方式
        if grant_type not in ('refresh_token',):
            return Response(data={'code': 403, 'msg': '不支持的授权方式'}, status=status.HTTP_403_FORBIDDEN)

        authorization = request.META.get('HTTP_AUTHORIZATION', None)
        if authorization is None:
            return Response(data={"msg": "缺失token"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh_token = authorization.split(' ')
        valid_refresh_token = TokenUtils.authenticate_refresh_token(refresh_token=refresh_token[1])

        if valid_refresh_token[0]:
            payload = {"uid": valid_refresh_token[1].get('uid', None),
                       'username': valid_refresh_token[1].get('username', None)
                       }
            tokens = TokenUtils.create_token(payload=payload)
            tokens['uid'] = valid_refresh_token[1].get('uid', None)
            tokens['nick_name'] = valid_refresh_token[1].get('username', None)
            del tokens['refresh_token']

        return Response(tokens)


class OauthESBViewSet(viewsets.GenericViewSet):
    """
    示例:http://127.0.0.1:8000/api/oauth/authorize/?client_id=p2pweb&client_secret=fgsdgrf&grant_type=refresh_token&username=zhiming&password=123456
    """

    # 限制请求频率
    throttle_scope = "esb_access_token"

    @action(methods=('get',), detail=False)
    def authorize(self, request, *args, **kwargs):
        # 授权类型
        tokens = None
        grant_type = request.GET.get('grant_type', None)
        # 客户端准入标识
        client_id = request.GET.get('client_id', None)
        # 客户端秘钥
        client_secret = request.GET.get('client_secret', None)

        # 判断授权方式
        if grant_type not in ('password', 'refresh_token'):
            return Response(data={'code': 403, 'msg': '不支持的授权方式'}, status=status.HTTP_403_FORBIDDEN)

        # 走密码方式授权获取token
        if grant_type == 'password':
            # 用户名
            username = request.GET.get('username', None)
            # 密码
            password = request.GET.get('password', None)
            # 验证密码
            user = authenticate(username=username, password=password)
            if user is None:
                return Response({'code': status.HTTP_401_UNAUTHORIZED, 'msg': '用户名或密码不正确!'}, status=status.HTTP_401_UNAUTHORIZED)

            # 查询系统信息
            sql = f"select top 1 system_code, system_name, software_provider_code, software_provider_name, org_code, org_name " \
                  f"from auth where appid='{user.uid}'"
            item = sql_exector.exec_query(sql)[0]

            payload = {"uid": user.uid,
                       'username': user.username,
                       "system_code": item[0],
                       "system_name": item[1],
                       "software_provider_code": item[2],
                       "software_provider_name": item[3],
                       "org_code": item[4],
                       "org_name": item[5]
                       }
            tokens = TokenUtils.create_token(payload=payload, token_timeout=7200 * 12)
            tokens['uid'] = user.uid
            tokens['nick_name'] = user.username

        #     刷新令牌
        elif grant_type == "refresh_token":
            authorization = request.META.get('HTTP_AUTHORIZATION', None)
            if authorization is None:
                return Response(data={"msg": "缺失token"}, status=status.HTTP_401_UNAUTHORIZED)

            refresh_token = authorization.split(' ')
            valid_refresh_token = TokenUtils.authenticate_refresh_token(refresh_token=refresh_token[1])

            if valid_refresh_token[0]:
                # 查询系统信息
                sql = f"select top 1 system_code, system_name, software_provider_code, software_provider_name, org_code, org_name " \
                      f"from auth where appid='{valid_refresh_token[1].get('uid', None)}'"

                result = sql_exector.exec_query(sql)
                if not result:
                    return Response(data={"msg": "签名正确,缺失用户信息"}, status=status.HTTP_403_FORBIDDEN)
                item = result[0]

                payload = {"uid": valid_refresh_token[1].get('uid', None),
                           'username': valid_refresh_token[1].get('username', None),
                           "system_code": item[0],
                           "system_name": item[1],
                           "software_provider_code": item[2],
                           "software_provider_name": item[3],
                           "org_code": item[4],
                           "org_name": item[5]
                           }
                tokens = TokenUtils.create_token(payload=payload, token_timeout=7200*12)
                tokens['uid'] = valid_refresh_token[1].get('uid', None)
                tokens['nick_name'] = valid_refresh_token[1].get('username', None)
                del tokens['refresh_token']

        # 保存到数据库
        gmt_iat = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        gmt_exp = (datetime.datetime.now() + datetime.timedelta(seconds=7200 * 12)).strftime(
            "%Y-%m-%d %H:%M:%S")

        sql_update = f"update auth set token='{tokens['access_token']}', gmt_exp='{gmt_exp}', gmt_iat='{gmt_iat}' where appid='{tokens['uid']}'"
        sql_exector.exec_update(sql_update)

        return Response(tokens)


class OauthESBV2ViewSet(viewsets.GenericViewSet):
    """
    示例:http://127.0.0.1:8000/api/oauth/authorize/?client_id=p2pweb&client_secret=fgsdgrf&grant_type=refresh_token&username=zhiming&password=123456
    """

    # 限制请求频率
    throttle_scope = "esb_access_token"

    @action(methods=('get',), detail=False, url_path='authorize')
    def authorize(self, request, username, password, grant_type, client_id=None, client_secret=None, *args, **kwargs):
        """
        走密码方式授权获取token
        :param client_secret: 客户端秘钥
        :param client_id: 客户端接入标识
        :param grant_type: 授权类型
        :param password: 资源拥有者密码
        :param username: 资源拥有者用户名
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 判断授权方式
        if grant_type not in ('password', ):
            return Response(data={'code': 403, 'msg': '不支持的授权方式'}, status=status.HTTP_403_FORBIDDEN)
        # 验证密码
        user = authenticate(username=username, password=password)
        if user is None:
            return Response({'code': status.HTTP_401_UNAUTHORIZED, 'msg': '用户名或密码不正确!'},
                            status=status.HTTP_401_UNAUTHORIZED)

        # 查询系统信息
        sql = f"select top 1 system_code, system_name, software_provider_code, software_provider_name, org_code, org_name " \
              f"from auth where appid='{user.uid}'"

        item = sql_exector.exec_query(sql)[0]

        payload = {"uid": user.uid,
                   'username': user.username,
                   "system_code": item[0],
                   "system_name": item[1],
                   "software_provider_code": item[2],
                   "software_provider_name": item[3],
                   "org_code": item[4],
                   "org_name": item[5]
                   }
        tokens = TokenUtils.create_token(payload=payload, token_timeout=7200 * 12)
        tokens['uid'] = user.uid
        tokens['nick_name'] = user.username

        # 保存到数据库
        gmt_iat = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        gmt_exp = (datetime.datetime.now() + datetime.timedelta(seconds=7200 * 12)).strftime(
            "%Y-%m-%d %H:%M:%S")

        sql_update = f"update auth set token='{tokens['access_token']}', gmt_exp='{gmt_exp}', gmt_iat='{gmt_iat}' where appid='{tokens['uid']}'"
        sql_exector.exec_update(sql_update)

        return Response(tokens)

    @action(methods=('get',), detail=False, url_path="refresh-token")
    def refresh_token(self, request, grant_type, client_id=None, client_secret=None, *args, **kwargs):
        """
        通过刷新令牌来更新请求token
        :param client_secret: 客户端秘钥
        :param client_id: 客户端接入标识
        :param grant_type: 授权类型
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 授权类型
        tokens = None
        # 判断授权方式
        if grant_type not in ('refresh_token',):
            return Response(data={'code': 403, 'msg': '不支持的授权方式'}, status=status.HTTP_403_FORBIDDEN)

        authorization = request.META.get('HTTP_AUTHORIZATION', None)
        if authorization is None:
            return Response(data={"msg": "缺失token"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh_token = authorization.split(' ')
        valid_refresh_token = TokenUtils.authenticate_refresh_token(refresh_token=refresh_token[1])

        if valid_refresh_token[0]:
            # 查询系统信息
            sql = f"select top 1 system_code, system_name, software_provider_code, software_provider_name, org_code, org_name " \
                  f"from auth where appid='{valid_refresh_token[1].get('uid', None)}'"
            result = sql_exector.exec_query(sql)
            if not result:
                return Response(data={"msg": "签名正确,缺失用户信息"}, status=status.HTTP_403_FORBIDDEN)
            item = result[0]

            payload = {"uid": valid_refresh_token[1].get('uid', None),
                       'username': valid_refresh_token[1].get('username', None),
                       "system_code": item[0],
                       "system_name": item[1],
                       "software_provider_code": item[2],
                       "software_provider_name": item[3],
                       "org_code": item[4],
                       "org_name": item[5]
                       }
            tokens = TokenUtils.create_token(payload=payload)
            tokens['uid'] = valid_refresh_token[1].get('uid', None)
            tokens['nick_name'] = valid_refresh_token[1].get('username', None)
            del tokens['refresh_token']

            # 保存到数据库
            gmt_iat = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            gmt_exp = (datetime.datetime.now() + datetime.timedelta(seconds=7200 * 12)).strftime(
                "%Y-%m-%d %H:%M:%S")

            sql_update = f"update auth set token='{tokens['access_token']}', gmt_exp='{gmt_exp}', gmt_iat='{gmt_iat}' where appid='{tokens['uid']}'"
            sql_exector.exec_update(sql_update)

        return Response(tokens)


# Create your views here.
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        # 获取用户名密码
        username = request.data.get('username')
        password = request.data.get('password')
        # 获取User对象
        try:
            # user = models.User.objects.filter(username=name, password=pwd).first()
            user = authenticate(username=username, password=password)
            if user is None:
                raise Exception('用户为空')
        except Exception as e:
            return Response({'status': 1, 'errmsg': '用户名或密码不正确!'})
        # 获取token
        payload = TokenUtils.create_token(payload={'uid': user.id}, token_timeout=1)
        # 返回成功响应
        return Response({'status': 0, 'token': payload})

    def get(self, request, *args, **kwargs):
        # 获取refresh_token
        refresh_token = request.META.get('HTTP_AUTHORIZATION', None).split(' ')[1]
        if refresh_token is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # 验证token
        payload = TokenUtils.authenticate_refresh_token(refresh_token=refresh_token)

        access_token = TokenUtils.create_token({"uid": 1})
        # 去除刷新token
        del access_token['refresh_token']
        return Response(access_token)
