#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""=================================================
    @Project: settings.py
    @File： account.py
    @Author：liaozhimingandy
    @Email: liaozhimingandy@gmail.com
    @Date：2024-04-18 15:35
    @Desc: 
================================================="""
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
from django.db.models import Q
from django.shortcuts import get_object_or_404
from ninja import Router, ModelSchema, Schema
from ninja.responses import codes_2xx, codes_4xx
from django.utils import timezone

from account.models import Account

# from account.api import router_account as router
router = Router(tags=["account"])


class AccountSchemaIn(ModelSchema):
    class Meta:
        model = Account
        fields = ['nick_name', 'email', 'gmt_birth', 'mobile', 'sex', 'avatar', 'password',
                  'allow_beep', 'allow_vibration']
        fields_optional = ["email", "gmt_birth", "mobile", 'sex', 'avatar', 'allow_beep', 'allow_vibration', 'password']


class MessageSchemaOut(Schema):
    message: str


class AccountSchemaOut(ModelSchema):
    class Meta:
        model = Account
        fields = ['username', 'nick_name', 'email', 'gmt_birth', 'areaCode', 'mobile', 'sex', 'avatar', 'is_active',
                  'user_type', 'allow_add_friend', 'allow_beep', 'allow_vibration',
                  'gmt_created', 'im_id', 'gmt_modified']

    @staticmethod
    def resolve_gmt_created(obj):
        # 重新处理时间为北京时间
        return timezone.localtime(obj.gmt_created)

    @staticmethod
    def resolve_gmt_modified(obj):
        # 重新处理时间为北京时间
        return timezone.localtime(obj.gmt_modified)


class AccountPasswordIn(Schema):
    username: str
    current_password: str = None
    password: str


@router.post("/register/", response={codes_2xx: AccountSchemaOut, codes_4xx: MessageSchemaOut})
def create_account(request, payload: AccountSchemaIn):
    """
    用户注册
    :param request:
    :param payload:
    :return:
    """
    payload_dict = payload.dict(exclude_unset=True)
    try:
        account = Account(**payload_dict)
        account.save()
    except ValidationError as e:
        return 400, {"message": str(e)}
    else:
        return 200, account


@router.post("/password/change/", response={codes_2xx: AccountSchemaOut, codes_4xx: MessageSchemaOut})
def password_change(request, payload: AccountPasswordIn):
    """
    密码修改
    :param request:
    :param payload:
    :return:
    """
    payload_dict = payload.dict()
    account = get_object_or_404(Account, username=payload_dict["username"].replace(settings.PREFIX_ID, ''), )
    try:
        # 检查密码
        assert check_password(payload_dict["current_password"], account.password), "Current password is incorrect."
    except AssertionError as e:
        return 400, {"message": str(e)}
    # 设置密码
    account.password = make_password(payload_dict["password"])
    account.save()
    return account


@router.post("/password/reset/", response=AccountSchemaOut)
def password_reset(request, payload: AccountPasswordIn):
    """
    密码重置
    :param request:
    :param payload:
    :return:
    """
    payload_dict = payload.dict()
    account = get_object_or_404(Account, username=payload_dict["username"].replace(settings.PREFIX_ID, ''))
    # 设置密码
    account.password = make_password(payload_dict["password"])
    account.save()
    return account


@router.get('/{username}/', response=AccountSchemaOut)
def get_account(request, username: str):
    """
    获取用户信息
    :param request:
    :param username:
    :return:
    """
    account = get_object_or_404(Account, username=username)
    return account


@router.put('/{username}/', response=AccountSchemaOut)
def update_account(request, username: str, payload: AccountSchemaIn):
    """
    更新用户信息
    :param payload:
    :param request:
    :param username:
    :return:
    """
    account = get_object_or_404(Account, username=username)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(account, attr, value)
    account.save()
    return account


@router.get('/search/{keyword}/')
def account_search(request, keyword: str):
    return Account.objects.filter(Q(username__icontains=keyword) | Q(nick__icontains=keyword))


if __name__ == "__main__":
    pass
