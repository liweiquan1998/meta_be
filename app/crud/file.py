import io
import time
from pathlib import Path
from typing import List
import magic
from fastapi.responses import StreamingResponse
from app.db.minio import FileHandler
from app import models, schemas
from sqlalchemy.orm import Session
from app.crud.basic import update_to_db
from app.common.validation import *
from app.core.storage.file import NfsStorage, MinioStorage

nfs = NfsStorage()
minio = MinioStorage()


def upload_nfs_file(file):
    return nfs.upload_file(file)


def upload_minio_file(file):
    return minio.upload_file(file)


def get_file(path: str):
    if 'minio' in path:
        return get_minio_file(path.split('minio/')[-1])
    elif 'nfs' in path:
        return get_nfs_file(path.split('nfs/')[-1])
    else:
        raise Exception(404, f'path:{path},文件路径不合法，应包含"minio"或"nfs"')


def get_nfs_file(path: str):
    return nfs.get_file(path)


def get_minio_file(path: str):
    return minio.get_file(path)


def get_minio_file_byte(path: str):
    return minio.get_file_byte(path)
