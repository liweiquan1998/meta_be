from fastapi.responses import StreamingResponse
from app.core.storage.file import NfsStorage, MinioStorage

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
    io_content, content_type = nfs.get_content(path)
    return StreamingResponse(io_content, media_type=content_type)


def get_minio_file(path: str):
    io_content, content_type = minio.get_content(path)
    return StreamingResponse(io_content, media_type=content_type)


def get_minio_file_byte(path: str):
    return minio.get_file_byte(path)
