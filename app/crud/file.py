import io
import time
from pathlib import Path
from typing import List

import magic
from fastapi.responses import StreamingResponse

from app import models, schemas
from sqlalchemy.orm import Session
from app.crud.basic import update_to_db
from app.common.validation import *


def get_nfs_file(path: str):
    file_path = Path('/mnt/nfs') / Path(path)
    with file_path.open('rb') as f:
        file_byte = f.read()
    content_type = magic.from_buffer(file_byte, mime=True)
    if file_byte:
        return StreamingResponse(io.BytesIO(file_byte), media_type=content_type)
    else:
        raise Exception(404, f"文件 {path} 不存在")

def upload_file(file):
    file_byte = file.file.read()
    file_name = f'{int(time.time())}{Path(file.filename).suffix}'
    result = Path(f'metaverse_assets/SceneAssets/{time.strftime("%Y%m", time.localtime())}')
    sys_path = '/mnt/nfs/' / result
    sys_path.mkdir(parents=True, exist_ok=True)
    real_path = sys_path / file_name
    try:
        with real_path.open('wb') as f:
            f.write(file_byte)
        real_path.chmod(0o777)
        return {'model': str(result / file_name)}
    except Exception as e:
        raise Exception(400, f"上传失败{e}")