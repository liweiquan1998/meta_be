import uuid
import random
import time
from pathlib import Path


class Handler(object):
    def __init__(self):
        self.nfs_uri_prefix = '/file/nfs'
        self.minio_uri_prefix = '/file/minio'

    # 生成nfs文件名称
    def get_nfs_name(self, file_name):
        nfs_name = f'{uuid.uuid1()}{Path(file_name).suffix}'
        return nfs_name

    # 写入nfs文件到指定目录
    def upload_nfs_file(self, real_path, file_byte):
        with real_path.open('wb') as f:
            f.write(file_byte)

    # 获取nfs文件的uri地址信息
    def get_nfs_uri(self, path_string):
        nfs_uri = self.nfs_uri_prefix + path_string
        return nfs_uri

    # 获取nfs文件信息
    def get_nfs_file(self, file_path):
        with file_path.open('rb') as f:
            file_byte = f.read()
        return file_byte

    # 生成minio文件名称
    def get_minio_name(self, file_name):
        minio_name = f'{time.strftime("%d%H%M%S", time.localtime())}{random.randint(1000, 9999)}{Path(file_name).suffix}'
        return minio_name

    # 获取minio文件的uri地址信息
    def get_minio_uri(self, path_string):
        minio_uri = self.minio_uri_prefix + path_string
        return minio_uri
