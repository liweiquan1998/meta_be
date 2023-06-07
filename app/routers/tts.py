import time
import uuid
from typing import List

from fastapi_pagination import paginate, Params
from sqlalchemy.orm import Session
from starlette.background import BackgroundTasks
from fastapi import Depends, File, UploadFile, Form
from app import schemas, get_db, crud, models
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
    tts_list = crud.get_tts_by_text_content(db, item.text_content, user)
    if len(tts_list) > 0:
        raise Exception("该内容已经存在，请勿重复创建")
    # 创建素材库的时候，为每一条语音创建两个素材库
    # 先给这个内容分配一个uuid
    text_id = uuid.uuid1()
    # 先创建一个男声的素材
    sex_1 = 1
    crud.create_tts(db, item, text_id, sex_1, background_tasks, user)
    # 再创建一个女声的素材
    sex_2 = 0
    crud.create_tts(db, item, text_id, sex_2, background_tasks, user)
    res = crud.get_tts_by_text_id(db, str(text_id))
    return res


@router_tts.get("/{text_id}", summary="获取指定uuid的tts")
@web_try()
@sxtimeit
def get_tts_by_text_id(text_id: str, db: Session = Depends(get_db), user=Depends(check_user)):
    res = crud.get_tts_by_text_id(db, text_id)
    return res


@router_tts.post("/tts_nfs_content", summary="文件上传nfs并更新数据", )
@web_try()
@sxtimeit
def upload_tts_content(file: UploadFile = File(...), params: str = Form(...), db: Session = Depends(get_db)):
    return crud.tts_file_content(file=file, params=params, db=db)


@router_tts.get("", summary="获取全部tts列表")
@web_try()
@sxtimeit
def get_tts(params: schemas.TTSParams = Depends(), db: Session = Depends(get_db), user=Depends(check_user)):
    # 先筛选获取全部的符合条件的tts列表
    tts_list = crud.get_tts_by_key_and_role(db, user, params.key, params.role)
    item_dict = {}
    for item in tts_list:
        if item.text_id not in item_dict.keys():
            item_dict[item.text_id] = [item]
        else:
            item_dict[item.text_id].append(item)
    res = []
    for key, value in item_dict.items():
        if len(value) != 2:
            continue
        value = sorted(value, key=lambda x: x.sex)
        status = 1 if value[0].status == 1 and value[1].status == 1 else 0
        tts_time = int(time.time()) - value[0].create_time
        if status == 0 and tts_time >= 3600: status = 2
        res.append({"text_content": value[0].text_content, "text_id": key, "status": status,
                    "role": value[0].role, "url_female": value[0].config_uri, "url_male": value[1].config_uri})
    return paginate(res, params)


@router_tts.delete("/{text_id}", summary="删除tts")
@web_try()
@sxtimeit
def delete_tts(text_id: str, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.delete_tts(db, text_id)
