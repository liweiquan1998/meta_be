from app.core.storage.file import NfsStorage, MinioStorage

nfs = NfsStorage()
minio = MinioStorage()


def upload_nfs_file(file):
    '''
    file_byte = file.file.read()
    file_name = handler.get_nfs_name(file.filename)
    result = Path('SceneAssets') / f'{time.strftime("%Y%m", time.localtime())}'
    sys_path = sys_prefix / result
    sys_path.mkdir(parents=True, exist_ok=True)
    real_path = sys_path / file_name
    try:
        handler.upload_nfs_file(real_path, file_byte)
        real_path.chmod(0o777)
        uri = handler.get_nfs_uri(str(result / file_name))
        return {'uri': uri}
    except Exception as e:
        raise Exception(400, f"上传失败{e}")
    '''
    return nfs.upload_file(file)


def upload_minio_file(file):
    # file_byte = file.file.read()
    # file_name = handler.get_minio_name(file.filename)
    # result = Path(time.strftime("%Y%m", time.localtime()))
    # real_path = result / file_name
    # path = FMH.put_file(real_path, file_byte)
    # uri = handler.get_minio_uri(path)
    # return {'uri': uri}
    return minio.upload_file(file)


def get_file(path: str):
    if 'minio' in path:
        return get_minio_file(path.split('minio/')[-1])
    elif 'nfs' in path:
        return get_nfs_file(path.split('nfs/')[-1])
    else:
        raise Exception(404, f'path:{path},文件路径不合法，应包含"minio"或"nfs"')


def get_nfs_file(path: str):
    # 兼容老地址
    # path = path.split("metaverse_assets/")[-1]
    # file_path = Path(sys_prefix) / Path(path)
    # file_byte = handler.get_nfs_file(file_path)
    # content_type = magic.from_buffer(file_byte, mime=True)
    # if file_byte:
    #     return StreamingResponse(io.BytesIO(file_byte), media_type=content_type)
    # else:
    #     raise Exception(404, f"文件 {path} 不存在")
    return nfs.get_file(path)


def get_minio_file(path: str):
    # file_byte = FMH.get_file(path)
    # content_type = magic.from_buffer(file_byte, mime=True)
    # if file_byte:
    #     return StreamingResponse(io.BytesIO(file_byte), media_type=content_type)
    # else:
    #     raise Exception(404, f"文件 {path} 不存在")
    return minio.get_file(path)


def get_minio_file_byte(path: str):
    # file_byte = FMH.get_file(path)
    # if file_byte:
    #     return file_byte
    # else:
    #     raise Exception(404, f"文件 {path} 不存在")
    return minio.get_file_byte(path)
