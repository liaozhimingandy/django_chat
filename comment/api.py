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
        fields = ['is_root', 'parent', 'content', 'account', "post", "app"]


class CommentSchemaOut(ModelSchema):
    app_id: str
    account_id: str
    post_id: int

    class Meta:
        model = Comment
        exclude = ['account', "post", "app"]

    @staticmethod
    def resolve_gmt_created(obj):
        # 重新处理时间为本地时间
        return timezone.localtime(obj.gmt_created)


@router.post("/", response=CommentSchemaOut)
def create_comment(request, payload: CommentSchemaIn):
    """
    添加评论
    :param request:
    :param payload:
    :return:
    """
    payload_dict = payload.dict()

    payload_dict.update(**{"app_id": payload_dict["app"], "post_id": payload_dict["post"],
                           "account_id": payload_dict["account"]})
    payload_dict.pop("account")
    payload_dict.pop("app")
    payload_dict.pop("post")
    comment = Comment(**payload_dict)
    comment.save()
    return comment


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


@router.delete("/{comment_id}/", response={204: None})
def delete_comment(request, comment_id: str):
    """
    删除指定的评论
    :param account_id:
    :param request:
    :param comment_id:
    :return:
    """
    if Comment.objects.filter(pk=comment_id).exists():
        comment = Comment.objects.get(pk=comment_id)
        comment.delete()

    return 204,


@router.get("/{app_id}/{post_id}/count/")
def get_comment_count(request, app_id: str, post_id: str):
    """
    获取指定帖子的评论数<br>
    :param request: <br>
    :param app_id: 应用ID<br>
    :param post_id: 帖子ID<br>
    :return: <br>
    """
    _count = Comment.objects.filter(app_id=app_id, post_id=post_id).count()
    return {"count": _count}


if __name__ == "__main__":
    pass
