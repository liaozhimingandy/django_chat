from django.contrib.auth import authenticate
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, status

from user.lib.TokenUtil import TokenUtils


class OauthViewSet(viewsets.GenericViewSet):
    """
    http://127.0.0.1:8000/api/oauth/authorize/?client_id=p2pweb&client_secret=fgsdgrf&grant_type=refresh_token&username=zhiming&password=123456
    """

    @action(methods=('get',), detail=False)
    def authorize(self, request, *args, **kwargs):
        # 授权类型
        tokens = None
        grant_type = request.GET.get('grant_type', None)
        # 客户端准入标识
        client_id = request.GET.get('client_id', None)
        # 客户端秘钥
        client_secret = request.GET.get('client_secret', None)
        # 走密码方式授权获取token
        if grant_type == 'password':
            # 用户名
            username = request.GET.get('username', None)
            # 密码
            password = request.GET.get('password', None)
            # 验证密码
            user = authenticate(username=username, password=password)
            if user is None:
                return Response({'status': 1, 'errmsg': '用户名或密码不正确!'}, status=status.HTTP_401_UNAUTHORIZED)

            payload = {"uid": user.id, 'username': user.username}
            tokens = TokenUtils.create_token(payload=payload)
            tokens['uid'] = user.id
            tokens['nick_name'] = user.username
        #     刷新令牌
        elif grant_type == "refresh_token":
            authorization = request.META.get('HTTP_AUTHORIZATION', None)
            if authorization is None:
                return Response(data={"msg": "缺失token"}, status=status.HTTP_401_UNAUTHORIZED)

            refresh_token = authorization.split(' ')
            valid_refresh_token = TokenUtils.authenticate_refresh_token(refresh_token=refresh_token[1])

            if valid_refresh_token[0]:
                payload = {"uid": valid_refresh_token[1].get('uid', None), 'username': valid_refresh_token[1].get('username', None)}
                tokens = TokenUtils.create_token(payload=payload)
                tokens['uid'] = valid_refresh_token[1].get('uid', None)
                tokens['nick_name'] = valid_refresh_token[1].get('username', None)
                del tokens['refresh_token']

        return Response(tokens)


# Create your views here.
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        # 获取用户名密码
        user_name = request.data.get('username')
        password = request.data.get('password')
        # 获取User对象
        try:
            # user = models.User.objects.filter(username=name, password=pwd).first()
            user = authenticate(username=user_name, password=password)
            if user is None:
                raise Exception('用户为空')
        except Exception as e:
            return Response({'status': 1, 'errmsg': '用户名或密码不正确!'})
        # 获取token
        payload = TokenUtils.create_token({'uid': user.id})
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
