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
    file_path = Path('/mnt/nfs/') / Path(path)
    with file_path.open('rb') as f:
        file_byte = f.read()
    content_type = magic.from_buffer(file_byte, mime=True)
    if file_byte:
        return StreamingResponse(file_byte, media_type=content_type)
    else:
        raise Exception(404, f"文件 {path} 不存在")

