#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""=================================================
    @Project: django_chat
    @File： serializers.py
    @Author：liaozhimingandy
    @Email: liaozhimingandy@gmail.com
    @Date：2024-06-18 8:20
    @Desc: 
================================================="""

from rest_framework import serializers

from account.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ["id", ]


if __name__ == "__main__":
    pass
