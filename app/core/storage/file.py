import io
import random
import time
import uuid
from typing import Tuple
import magic
from pathlib import Path
from app.db.minio import FileHandler
from configs.setting import config

from app.core.storage.base import FileStorage

nfs_prefix = config.get("nfs", "sys_prefix")
FMH = FileHandler("metaverse")


class NfsStorage(FileStorage):
    def get_name(self, file_name) -> str:
        file_name = f'{uuid.uuid1()}{Path(file_name).suffix}'
        return file_name

    def get_uri(self, end_nfs) -> str:
        uri = '/file/nfs/' + end_nfs
        return uri

    def upload(self, file) -> dict:
        file_byte = file.file.read()
        file_name = self.get_name(file.filename)
        result = Path('SceneAssets') / f'{time.strftime("%Y%m", time.localtime())}'
        sys_path = nfs_prefix / result
        sys_path.mkdir(parents=True, exist_ok=True)
        real_path = sys_path / file_name
        try:
            with real_path.open('wb') as f:
                f.write(file_byte)
            real_path.chmod(0o777)
            uri = self.get_uri(str(result / file_name))
            return {'uri': uri}
        except Exception as e:
            raise Exception(400, f"上传文件失败{e}")

    def get_content(self, path) -> Tuple[io.BytesIO, str]:
        # 兼容老地址
        path = path.split("metaverse_assets/")[-1]
        file_path = Path(nfs_prefix) / Path(path)
        with file_path.open('rb') as f:
            file_byte = f.read()
        content_type = magic.from_buffer(file_byte, mime=True)
        if file_byte:
            return io.BytesIO(file_byte), content_type
        else:
            raise Exception(404, f"文件 {path} 不存在")


class MinioStorage(FileStorage):
    def get_name(self, file_name) -> str:
        file_name = f'{time.strftime("%d%H%M%S", time.localtime())}{random.randint(1000, 9999)}{Path(file_name).suffix}'
        return file_name

    def get_uri(self, end_minio) -> str:
        uri = '/file/minio/' + end_minio
        return uri

    def upload(self, file) -> dict:
        file_byte = file.file.read()
        file_name = self.get_name(file.filename)
        result = Path(time.strftime("%Y%m", time.localtime()))
        real_path = result / file_name
        path = FMH.put_file(real_path, file_byte)
        uri = self.get_uri(path)
        return {'uri': uri}

    def get_content(self, path) -> Tuple[io.BytesIO, str]:
        file_byte = FMH.get_file(path)
        content_type = magic.from_buffer(file_byte, mime=True)
        if file_byte:
            return io.BytesIO(file_byte), content_type
        else:
            raise Exception(404, f"文件 {path} 不存在")

    def get_file_byte(self, path):
        file_byte = FMH.get_file(path)
        if file_byte:
            return file_byte
        else:
            raise Exception(404, f"文件 {path} 不存在")
