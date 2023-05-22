import uuid

from fastapi_pagination import paginate, Params
from sqlalchemy.orm import Session
from starlette.background import BackgroundTasks
from fastapi import Depends, File, UploadFile, Form
from app import schemas, get_db, crud
from app.common.validation import check_user
from utils import web_try, sxtimeit
from fastapi import Depends
from fastapi import APIRouter

router_tts = APIRouter(
    prefix="/tts",
    tags=["tts-文字转语音管理"],
)


@router_tts.post("", summary="创建tts")
@web_try()
@sxtimeit
def add_tts(item: schemas.TTSCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db),
            user=Depends(check_user)):
    # 创建素材库的时候，为每一条语音创建两个素材库
    # 先给这个内容分配一个uuid
    text_id = uuid.uuid1()
    # 先创建一个男声的素材
    sex_1 = 1
    crud.create_tts(db, item, text_id, sex_1, background_tasks)
    # 再创建一个女声的素材
    sex_2 = 0
    crud.create_tts(db, item, text_id, sex_2, background_tasks)
    res = crud.get_tts_by_text_id(db, str(text_id))
    return res


@router_tts.get("/{text_id}", summary="获取指定uuid的tts")
@web_try()
@sxtimeit
def get_tts_by_text_id(text_id: str, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.get_tts_by_text_id(db, text_id)


@router_tts.post("/tts_nfs_content", summary="文件上传nfs并更新数据", )
@web_try()
@sxtimeit
def upload_tts_content(file: UploadFile = File(...), params: str = Form(...), db: Session = Depends(get_db)):
    # , user=Depends(check_user)):
    return crud.tts_file_content(file=file, params=params, db=db)


@router_tts.get("", summary="获取全部tts列表")
@web_try()
@sxtimeit
def get_tts(params: Params = Depends(), db: Session = Depends(get_db), user=Depends(check_user)):
    return paginate(crud.get_all_tts(db), params)


@router_tts.delete("/{text_id}", summary="删除tts")
@web_try()
@sxtimeit
def delete_tts(text_id: str, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.delete_tts(db, text_id)
