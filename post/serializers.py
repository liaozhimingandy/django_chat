#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""=================================================
    @Project: django_chat
    @File： serializers.py.py
    @Author：liaozhimingandy
    @Email: liaozhimingandy@gmail.com
    @Date：2024-06-17 13:59
    @Desc: 
================================================="""
from rest_framework import serializers

from post.models import Post, Like, Comment, Image


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ["id", ]


class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        exclude = ["id", ]

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        exclude = ["id", ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ["id"]


if __name__ == "__main__":
    pass
