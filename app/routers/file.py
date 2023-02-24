from concurrent.futures import ThreadPoolExecutor

from fastapi_pagination import paginate, Params
from sqlalchemy.orm import Session

from app import schemas, get_db, crud
from app.common.validation import check_user
from utils import web_try, sxtimeit
from fastapi import FastAPI, File, UploadFile, Form
from fastapi import Depends
from fastapi import APIRouter
from typing import List
from app.common.validation import *
from app.common.validation import *

router_file = APIRouter(
    prefix="/file",
    tags=["file-文件管理"],
)


# 单个文件

@router_file.post("/NfsFile", summary="nfs上传文件")
@web_try()
@sxtimeit
def upload_file(file: UploadFile = File(...)):
    # , user=Depends(check_user)):
    return crud.upload_nfs_file(file)


@router_file.post('/MinioFile', summary="minio上传文件")
@web_try()
@sxtimeit
def upload_minio_file(file: UploadFile = File(...), params: dict = Form(...), db: Session = Depends(get_db)):
    # , user=Depends(check_user)):
    return crud.upload_minio_file(file=file, params=params, db=db, model_cls=models.MarketingContent)


@router_file.get("/{uri:path}", summary="获取文件")
@sxtimeit
def get_nfs_file(uri):
    return crud.get_file(uri)


# @router_file.get("/NfsFile/{uri:path}", summary="nfs获取文件")
# @sxtimeit
# def get_nfs_file(uri):
#     return crud.get_nfs_file(uri)
#
#
# @router_file.get("/MinioFile/{uri:path}", summary="minio获取文件")
# @sxtimeit
# def get_minio_file(uri):
#     return crud.get_minio_file(uri)


# 多个文件
@router_file.post("/MinioFiles", summary="minio上传多个文件")
async def create_files(files: List[UploadFile] = File(...)):
    # , user=Depends(check_user)):
    with ThreadPoolExecutor(max_workers=8) as executor:
        results = executor.map(crud.upload_minio_file, files)
    uris = [result['uri'] for result in results]
    # uris = [crud.upload_minio_file(file)['uri'] for file in files]
    return {'uris': uris}


@router_file.post("/NfsFiles", summary="nfs上传多个文件")
async def create_files(files: List[UploadFile] = File(...)):
    # , user=Depends(check_user)):
    with ThreadPoolExecutor(max_workers=8) as executor:
        results = executor.map(crud.upload_nfs_file, files)
    uris = [result['uri'] for result in results]
    # uris = [crud.upload_minio_file(file)['uri'] for file in files]
    return {'uris': uris}
