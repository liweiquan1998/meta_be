import io
from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists, NoSuchKey)
from configs.setting import config


class FileHandler(object):

    def __init__(self, bucket_name):
        self.bucket_name = bucket_name

        self.minio_client = Minio(config.get('minio_url'),
                                  access_key=config.get('minio_access_key'),
                                  secret_key=config.get('minio_secret_key'),
                                  secure=False)
        # 创桶
        try:
            self.minio_client.make_bucket(self.bucket_name)
        except BucketAlreadyExists:
            pass
        except BucketAlreadyOwnedByYou:
            pass
        except ResponseError as e:
            raise Exception("minio连接失败") from e

    def put_file(self, filename, filebyte):
        filename = str(filename)
        fileio = io.BytesIO(filebyte)
        try:
            self.minio_client.put_object(self.bucket_name, filename, fileio, len(filebyte))
            return filename
        except ResponseError as e:
            raise Exception(f"minio创建文件失败 文件名:{filename}") from e

    def get_file(self, filename):
        try:
            return self.minio_client.get_object(self.bucket_name, filename).data
        except ResponseError as e:
            raise Exception(f"minio获取文件失败 文件名:{filename}") from e
