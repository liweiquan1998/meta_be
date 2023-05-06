from concurrent.futures import ThreadPoolExecutor
from app import crud
from utils import web_try, sxtimeit
from fastapi import File, UploadFile
from fastapi import APIRouter
from typing import List

router_file = APIRouter(
    prefix="/file",
    tags=["file-文件管理"],
)


# 单个文件

@router_file.post("/NfsFile/{status}", summary="nfs上传文件")
@web_try()
@sxtimeit
def upload_file(status: int,file: UploadFile = File(...)):
    # , user=Depends(check_user)):
    return crud.upload_nfs_file(file,status)


@router_file.post('/MinioFile', summary="minio上传文件")
@web_try()
@sxtimeit
def upload_minio_file(file: UploadFile = File(...)):
    # , user=Depends(check_user)):
    return crud.upload_minio_file(file=file)


@router_file.get("/{uri:path}", summary="获取文件")
@sxtimeit
def get_nfs_file(uri):
    return crud.get_file(uri)


# 多个文件
@router_file.post("/MinioFiles", summary="minio上传多个文件")
async def create_files(files: List[UploadFile] = File(...)):
    # , user=Depends(check_user)):
    with ThreadPoolExecutor(max_workers=8) as executor:
        results = executor.map(crud.upload_minio_file, files)
    uris = [result['uri'] for result in results]
    return {'uris': uris}


@router_file.post("/NfsFiles/{status}", summary="nfs上传多个文件")
async def create_files(status: int,files: List[UploadFile] = File(...)):
    # , user=Depends(check_user)):
    if not status:
        status = 0
    with ThreadPoolExecutor(max_workers=8) as executor:
        results = executor.map(crud.upload_nfs_file, (files,status))
    uris = [result['uri'] for result in results]
    return {'uris': uris}
