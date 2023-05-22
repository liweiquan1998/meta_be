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
    tts_list = crud.get_all_tts(db)
    content_list = []
    res = []
    for item in tts_list:
        # 判断一下res中是否存在这个语音信息
        if item.text_content not in content_list:
            content_list.append(item.text_content)
            two_list = crud.get_tts_by_text_content(db, item.text_content)
            # 判断一下两个语音是否全部生成
            if two_list[0].status == 1 and two_list[1].status == 1:
                status = 1
            else:
                status = 0
            res.append({"text_content": item.text_content, "text_id": item.text_id, "status": status})
    return paginate(res, params)


@router_tts.delete("/{text_id}", summary="删除tts")
@web_try()
@sxtimeit
def delete_tts(text_id: str, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.delete_tts(db, text_id)
