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
from copy import deepcopy
from typing import List

from django.utils import timezone
from ninja import File, ModelSchema, Router
from ninja.files import UploadedFile

from post.lib.utils import get_uploaded_file_md5
from post.models import Image, Post

router = Router(tags=["post"])
router_image = Router(tags=["image"])


class PostSchemaIn(ModelSchema):
    class Meta:
        model = Post
        fields = ['content', 'from_device', 'right_status', 'location', 'is_top', 'latitude', 'longitude', 'status',
                  'account_id']
        fields_optional = ['right_status', "is_top", 'latitude', 'longitude', 'status']


class PostSchemaOut(ModelSchema):
    class Meta:
        model = Post
        exclude = ["id"]

    @staticmethod
    def resolve_gmt_created(obj):
        # 重新处理时间为北京时间
        return timezone.localtime(obj.gmt_created)


@router.get("/lasted/", response=List[PostSchemaOut])
def list_lasted_post(request):
    """
    获取最近的十条帖子数据
    :param app_id:
    :param request:
    :return:
    """
    posts = Post.objects.order_by('-id')[:10]
    return posts


@router.post("/", response=PostSchemaOut)
def create_post(request, payload: PostSchemaIn):
    """
    创建帖子
    :param request:
    :param payload:
    :return:
    """
    payload_dict = payload.dict(exclude_unset=True)
    payload_dict.update(**{"from_ip": request.META['REMOTE_ADDR']})
    post = Post(**payload_dict)
    post.save()

    return post


@router.delete("/{post_id}/", response={204: None})
def delete_post(request, post_id: str):
    """
    删除指定帖子
    :param request:
    :param post_id:
    :return:
    """
    Post.objects.filter(post_id=post_id).delete()
    return 204,


@router_image.post("/upload/")
def image_upload(request, file: UploadedFile = File(...)):
    """
    图片上传
    使用 form-data方式上传
    :param request:
    :param file:
    :return:
    """
    image_copy = deepcopy(file)
    image_md5 = get_uploaded_file_md5(image_copy)
    # 判断文件是否存在
    if not Image.objects.filter(image_md5=image_md5).exists():
        image = Image(image_name=file.name, image=file, image_md5=image_md5)
        image.save()
    else:
        image = Image.objects.get(image_md5=image_md5)

    return {"image_url": image.image.url}


if __name__ == "__main__":
    pass
