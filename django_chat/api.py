#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""=================================================
    @Project: settings.py
    @File： account.py
    @Author：liaozhimingandy
    @Email: liaozhimingandy@gmail.com
    @Date：2024-04-12 10:22
================================================="""

from ninja import NinjaAPI

from account.apis.oauth import router as router_oauth
from account.apis.account import router as router_account
from post.apis.post import router as router_post, router_image
from post.apis.comment import router as router_comment
from post.apis.like import router as router_like
from account.authentication import AuthBearer

# todo: 上线时开启auth=AuthBearer()
api = NinjaAPI(version='3.0', title='Chat API', description="内部接口文档",
               auth=None,
               openapi_extra={
                   "info": {
                       "terms Of Service": "https://api.chat.alsoapp.com/",
                   }}, docs_url="/docs/", servers=[
        {"url": "https://api-test.chat.alsoapp.com", "description": "测试环境"},
        {"url": "https://api.chat.alsoapp.com", "description": "生产环境"}, ])

api.add_router("/oauth/", router_oauth)
api.add_router("/account/", router_account)
api.add_router("/comments/", router_comment)
api.add_router("/posts/", router_post)
api.add_router("/likes/", router_like)
api.add_router("/image/", router_image)


# 异常
class ServiceUnavailableError(Exception):
    pass


@api.exception_handler(ServiceUnavailableError)
def service_unavailable(request, exc):
    return api.create_response(
        request,
        {"message": "Please retry later"},
        status=503,
    )


if __name__ == "__main__":
    pass
