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

from ninja import ModelSchema, Router

from post.models import Like

router = Router(tags=["like"])


class LikeSchema(ModelSchema):
    class Meta:
        model = Like
        fields = ["account_id", ]


@router.get("/{post_id}/{account_id}/count/")
def get_likes(request, post_id: str, account_id: str):
    """
    获取点赞数
    :param request:
    :param post_id: 帖子ID
    :param account_id: 当前用户
    :return:
    """
    count_like = Like.objects.filter(post_id=post_id).count()
    is_like = Like.objects.filter(post_id=post_id, account_id=account_id).exists()
    return {"count": count_like, "is_like": is_like}


@router.delete("/{post_id}/{account_id}/")
def delete_like(request, post_id: str, account_id: str):
    """
    取消点赞
    :param account_id: 当前用户
    :param request:
    :param post_id: 帖子ID
    :return:
    """
    Like.objects.filter(post_id=post_id, account_id=account_id).delete()
    count_like = Like.objects.filter(post_id=post_id).count()

    return {"count": count_like, "is_like": False}


@router.post("/{post_id}/")
def create_like(request, post_id: str, payload: LikeSchema):
    """
    点赞
    :param request:
    :param post_id:
    :param payload:
    :return:
    """
    payload_dict = payload.dict()

    Like(post_id=post_id, account_id=payload_dict["account_id"]).save()
    count_like = Like.objects.filter(post_id=post_id).count()

    return {"count": count_like, "is_like": True}


if __name__ == "__main__":
    pass
