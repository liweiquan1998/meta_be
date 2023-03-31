import os.path

from fastapi.responses import StreamingResponse
from app.core.storage.file import NfsStorage, MinioStorage
from pathlib import Path
from configs.setting import config

nfs_prefix = config.get("nfs", "sys_prefix")
nfs = NfsStorage()
minio = MinioStorage()


def upload_nfs_file(file):
    return nfs.upload(file)


def upload_minio_file(file):
    return minio.upload(file)


def get_file(path: str):
    if 'minio' in path:
        return get_minio_file(path.split('minio/')[-1])
    elif 'nfs' in path:
        return get_nfs_file(path.split('nfs/')[-1])
    else:
        raise Exception(404, f'path:{path},文件路径不合法，应包含"minio"或"nfs"')


def get_nfs_file(path: str):
    path = path.split("metaverse_assets/")[-1]
    file_path = Path(nfs_prefix) / Path(path)
    if os.path.exists(file_path):
        io_content, content_type = nfs.get_content(file_path)
        return StreamingResponse(io_content, media_type=content_type)
    else:
        return {'code': 400, 'msg': '图片不存在'}


def get_minio_file(path: str):
    io_content, content_type = minio.get_content(path)
    return StreamingResponse(io_content, media_type=content_type)


def get_minio_file_byte(path: str):
    return minio.get_file_byte(path)
