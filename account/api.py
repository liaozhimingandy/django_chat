#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""=================================================
    @Project: settings.py
    @File： api.py
    @Author：liaozhimingandy
    @Email: liaozhimingandy@gmail.com
    @Date：2024-04-18 15:35
    @Desc: 
================================================="""
from django.db.models import Q
from django.shortcuts import get_object_or_404
from ninja import Router, ModelSchema
from django.utils import timezone

from account.models import Account

router = Router(tags=["account"])


class AccountSchemaIn(ModelSchema):
    class Meta:
        model = Account
        fields = ['nick_name', 'email', 'gmt_birth', 'mobile', 'sex', 'avatar', 'password',
                  'allow_beep', 'allow_vibration']
        fields_optional = ["email", "gmt_birth", "mobile", 'sex', 'avatar', 'allow_beep', 'allow_vibration', 'password']


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


class AccountPassword(ModelSchema):
    current_password: str = None

    class Meta:
        model = Account
        fields = ["username", "password"]


@router.post("/register/", response=AccountSchemaOut)
def create_account_(request, payload: AccountSchemaIn):
    """
    用户注册
    :param request:
    :param payload:
    :return:
    """
    payload_dict = payload.dict(exclude_unset=True)
    account = Account(**payload_dict)
    account.save()
    return account


@router.post("/password/change/", response=AccountSchemaOut)
def password_change(request, payload: AccountPassword):
    """
    密码修改
    :param request:
    :param payload:
    :return:
    """
    payload_dict = payload.dict()
    account = get_object_or_404(Account, username=payload_dict["username"], password=payload_dict["current_password"])
    account.password = payload_dict["password"]
    account.save()
    return account


@router.post("/password/reset/", response=AccountSchemaOut)
def password_reset(request, payload: AccountPassword):
    """
    密码重置
    :param request:
    :param payload:
    :return:
    """
    payload_dict = payload.dict()
    account = get_object_or_404(Account, username=payload_dict["username"])
    account.password = payload_dict["password"]
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
