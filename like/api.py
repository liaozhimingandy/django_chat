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

from ninja import Router, ModelSchema
from ninja.orm import ModelSchema

from like.models import Like

router = Router(tags=["like"])


class LikeSchema(ModelSchema):
    class Meta:
        model = Like
        fields = ["uid"]


@router.get("/{app_id}/{post_id}/{uid}/")
def get_likes(request, app_id: str, post_id: str, uid: str):
    """
    获取点赞数
    :param request:
    :param app_id:
    :param post_id:
    :param uid:
    :return:
    """
    count_like = Like.objects.filter(app_id=app_id, post_id=post_id).count()
    is_like = Like.objects.filter(app_id=app_id, post_id=post_id, uid=uid).exists()
    return {"code": 200,  "message": "ok", "data": {"count": count_like, "is_like": is_like}}


@router.delete("/{app_id}/{post_id}/{uid}/")
def delete_like(request, app_id: str, post_id: str, uid: str):
    """
    取消点赞
    :param request:
    :param app_id:
    :param post_id:
    :return:
    """
    count_like = Like.objects.filter(app_id=app_id, post_id=post_id).count()
    Like.objects.filter(app_id=app_id, post_id=app_id, uid=uid).delete()
    return {"code": 200,  "message": "ok", "data": {"count": count_like, "is_like": False}}


@router.post("/{app_id}/{post_id}/")
def create_like(request, app_id: str, post_id: str, payload: LikeSchema):
    """
    点赞
    :param request:
    :param app_id:
    :param post_id:
    :param payload:
    :return:
    """
    payload_dict = payload.dict()
    Like(app_id=app_id, post_id=post_id, uid=payload_dict["uid"]).save()

    count_like = Like.objects.filter(app_id=app_id, post_id=post_id).count()

    return {"code": 201,  "message": "ok", "data": {"count": count_like, "is_like": True}}


if __name__ == "__main__":
    pass
