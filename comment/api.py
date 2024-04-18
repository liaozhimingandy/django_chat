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
from typing import List
from django.utils import timezone
from ninja import Router, ModelSchema
from ninja.pagination import paginate, LimitOffsetPagination

from comment.models import Comment

router = Router(tags=["comment"])


class CommentSchemaIn(ModelSchema):
    class Meta:
        model = Comment
        fields = ['is_root', 'pid', 'content', 'uid']


class CommentSchemaOut(ModelSchema):
    class Meta:
        model = Comment
        fields = "__all__"

    @staticmethod
    def resolve_gmt_created(obj):
        # 重新处理时间为本地时间
        return timezone.localtime(obj.gmt_created)


@router.post("/{app_id}/{post_id}/", response=CommentSchemaOut)
def create_comment(request, app_id: str, post_id: str, payload: CommentSchemaIn):
    """
    添加评论
    :param request:
    :param app_id:
    :param post_id:
    :param payload:
    :return:
    """
    payload_dict = payload.dict()
    payload_dict.update(**{"app_id": app_id, "post_id": post_id})
    comment = Comment(**payload_dict)
    comment.save()
    return comment


@router.delete("/{comment_id}/{uid}/", response={204: None})
def delete_comment(request, comment_id: str, uid: str):
    """
    删除指定的评论
    :param request:
    :param comment_id:
    :param uid:
    :return:
    """
    if Comment.objects.filter(pk=comment_id).exists():
        comment = Comment.objects.get(pk=comment_id)
        comment.delete()

    return 204,


@router.get("/{app_id}/{post_id}/", response=List[CommentSchemaOut])
@paginate(LimitOffsetPagination)
def list_comment(request, app_id: str, post_id: str):
    """
    分页返回评论列表
    :param request:
    :param app_id:
    :param post_id:
    :return:
    """
    comments = Comment.objects.filter(app_id=app_id, post_id=post_id).order_by("-id").all()
    return comments


if __name__ == "__main__":
    pass
