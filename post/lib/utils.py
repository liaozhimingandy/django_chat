import hashlib
import os
from datetime import datetime
import uuid
from pathlib import Path

from django.conf import settings
from django.core.files import File


# 接收并保存图片
def save_img(image, dest_father_dir):
    # 创建存储路径
    img_dir1 = os.path.join(settings.MEDIA_ROOT, dest_father_dir)
    if not os.path.exists(img_dir1):
        os.makedirs(img_dir1)
    img_dir2 = os.path.join(img_dir1, datetime.now().strftime("%Y"))
    if not os.path.exists(img_dir2):
        os.makedirs(img_dir2)
    img_file = os.path.join(img_dir2, datetime.now().strftime("%m"))
    if not os.path.exists(img_file):
        os.makedirs(img_file)

    # 防重名
    p = Path(image.name)
    img_pure_name = p.stem + '-' + str(uuid.uuid4()).replace('-', '')[:6]
    img_extend_name = p.suffix
    img_name = img_pure_name + img_extend_name

    # 存储图片
    destination = open(os.path.join(img_file, img_name), 'wb+')
    for chunk in image.chunks():
        destination.write(chunk)
    destination.close()

    return img_name


# 获取图片存储地址
def get_img_url(request, img_file, img_name):
    if request.is_secure():
        protocol = 'https'
    else:
        protocol = 'http'
    # 传回给后端ImageField要存储的图片路径
    backend_relative_path = settings.MEDIA_URL + img_file + '/' + datetime.now().strftime(
        "%Y") + '/' + datetime.now().strftime("%m") + '/' + img_name
    relative_path = backend_relative_path
    # 前端显示需要的图片路径
    frontend_url = protocol + '://' + str(request.META['HTTP_HOST']) + relative_path
    return {"url": frontend_url, "image_path": backend_relative_path}


def get_uploaded_file_md5(inmemory_file) -> str:
    """
    计算内存文件md5值
    :param inmemory_file: 内存文件对象
    :return: md5值
    """
    # 将InMemoryUploadedFile转换为File类型
    file = File(inmemory_file)

    # 计算文件的MD5值
    md5 = hashlib.md5()
    for chunk in file.chunks():
        md5.update(chunk)

    return md5.hexdigest()


def split_file_type(file):
    """
    对文件名切割，获取名字和类型
    """
    file_li = os.path.splitext(file)
    return file_li[0], file_li[1]
