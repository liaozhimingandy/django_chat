#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""=================================================
    @Project: settings.py
    @File： api.py
    @Author：liaozhimingandy
    @Email: liaozhimingandy@gmail.com
    @Date：2024-04-12 10:22
================================================="""
from ninja import NinjaAPI

from oauth.api import router as oauth_router
from account.api import router as account_router
from comment.api import router as comment_router
from post.api import router as post_router
from post.api import router_image
from like.api import router as like_router

api = NinjaAPI(version='1.0.0', title='Welink API')

api.add_router("/oauth/", oauth_router)
api.add_router("/account/", account_router)
api.add_router("/comments/", comment_router)
api.add_router("/posts/", post_router)
api.add_router("/likes/", like_router)
api.add_router("/image/", router_image)


if __name__ == "__main__":
    pass
