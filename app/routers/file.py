from fastapi_pagination import paginate, Params
from sqlalchemy.orm import Session

from app import schemas, get_db, crud
from app.common.validation import check_user
from utils import web_try, sxtimeit
from fastapi import FastAPI, File, UploadFile
from fastapi import Depends
from fastapi import APIRouter
from app.common.validation import *
from app.common.validation import *

router_file = APIRouter(
    prefix="/file",
    tags=["file-文件管理"],
)


@router_file.post("/uploadNfsFile", summary="nfs上传文件")
@web_try()
@sxtimeit
def upload_file(file: UploadFile = File(...)):
    return crud.upload_file(file)

@router_file.get("/getNfsFile/{uri:path}", summary="nfs获取文件")
@sxtimeit
def get_nfs_file(uri):
    return crud.get_nfs_file(uri)

