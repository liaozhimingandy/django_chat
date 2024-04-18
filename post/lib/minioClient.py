import copy
import os

from django.conf import settings
from minio import Minio

MINIO_CONF = {
    'endpoint': settings.MINIO_ENDPOINT,
    'access_key': settings.MINIO_ACCESS_KEY,
    'secret_key': settings.MINIO_SECRET_KEY,
    'secure': False
}

client = Minio(**MINIO_CONF)


def get_file_size(file):
    """
    获取文件大小
    file: bytes
    return: int
    """
    file.seek(0, os.SEEK_END)
    return file.tell()
    # im = io.BytesIO(file)
    # return im.getbuffer().nbytes


def go_upload_file(file, bucket='images', path_name=''):
    """
    上传文件,自动计算文件大小
    """
    try:
        # print(path_name)
        # print(type(file))
        file_len = get_file_size(copy.copy(file))
        # print(file_len)
        result = client.put_object(bucket_name=bucket, object_name=path_name, data=file, length=file_len)
        return result
    except(Exception, ) as e:
        return 0, None


def go_upload_file_have_size(file, size, bucket='images', path_name=''):
    """
    上传文件，已有文件大小
    """
    try:
        result = client.put_object(bucket_name=bucket, object_name=path_name, data=file, length=size)
        return result.etag, result.bucket_name
    except (Exception, ) as e:
        return 0, str(e)


def go_delete_file(bucket='media', path_name=''):
    """
    删除文件
    """
    try:
        # print(bucket, path_name)
        client.remove_object(bucket_name=bucket, object_name=path_name)
        return 1
    except Exception as e:
        print(e)
        return 0


def go_delete_file_list(bucket='media', path_name_list=[]):
    """
    删除文件列表
    未实现，据说需要删除完遍历结果
    """
    try:
        result = client.remove_objects(bucket, path_name_list)
        return 1
    except Exception as e:
        print(e)
        return 0


def get_file_url(bucket='media', path_name=''):
    """
    获取文件url
    """
    try:
        url = client.presigned_get_object(bucket_name=bucket, object_name=path_name)
        return url
    except Exception as e:
        print(e)
        return None


def get_file_path(path):
    path = path.split('/')[2:]
    final_path = '/'.join(path)
    return final_path
