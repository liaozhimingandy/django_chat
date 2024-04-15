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

api = NinjaAPI()

api.add_router("/oauth/", oauth_router)

if __name__ == "__main__":
    pass
