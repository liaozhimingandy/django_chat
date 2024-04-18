import os
import uuid
from io import BytesIO

from django.conf import settings
from django.core.files.storage import Storage

from .lib.minioClient import go_delete_file, go_upload_file_have_size


class MinioStorage(Storage):
    """
    自定义文件Minio存储系统
    """

    def get_created_time(self, name):
        pass

    def get_modified_time(self, name):
        pass

    def get_accessed_time(self, name):
        pass

    def size(self, name):
        pass

    def listdir(self, path):
        pass

    def path(self, name):
        pass

    def __init__(self, option=None):
        # 构造方法
        # 当在存储数据的时候, django会自动调用构造方法, 但是不会传参进来,
        if not option:
            self.bucket = settings.MINIO_BUCKET
            self.bucket = settings.MINIO_BUCKET
            self.endpoint = settings.MINIO_ENDPOINT
            self.schema = settings.MINIO_SCHEMA
            self.image_md5 = ''

    def _open(self, name, mode='rb'):
        """
        用打开文件的时候调用的
        因为此时,只需要进行文件的上传,不需要进行文件的下载,但是又必须要进行定义,
        只能在需要用到的时候,再使用,在此之前只好pass
        :param name: 要打开的文件的名字
        :param mode: 打开文件方式
        :return: None
        """
        pass

    def _save(self, name, content) -> str:
        """
        存储文件的时候调用的
        :param name: 要保存的文件名字
        :param content: 要保存的文件的内容
        :return: 保存的文件名称
        """
        # name = name.replace('\\', '/')
        path_dir = os.path.split(name)[0]
        name = f'{path_dir}/{uuid.uuid4()}{os.path.splitext(name)[1]}'
        result = go_upload_file_have_size(BytesIO(content.read()), content.size, bucket=self.bucket, path_name=name)
        assert result[0] != 0, f'file upload failed! error: {result[1]}'
        self.image_md5 = result[0]
        return name

    def delete(self, name):
        # 删除name的文件
        # im = get_file_path(instance.img)
        # print(name)
        # name = str(name).split('/')[-1]
        go_delete_file(bucket=self.bucket, path_name=str(name))
        # print(ret)

    def url(self, name):
        """
        返回文件的全路径
        该方法是提供给模型类中ImageField字段对应的属性调用的(file_id被存储到ImageField字段种中)
        :param name: 要读取文件的引用
        :return:
        """
        return f'{self.schema}{self.endpoint}/{self.bucket}/{name}'

    def exists(self, name):
        """
        判断文件是否已经在本地存储， 返回True表示文件已经存储在本地/django不会再去存储该文件
        返回False, 告诉Django这是一个新的文件，请你存储。
        只有返回False, django才会积极的存储文件到fdfs
        """
        return False
