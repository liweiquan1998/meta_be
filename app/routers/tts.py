from fastapi_pagination import paginate, Params
from sqlalchemy.orm import Session
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
def add_tts(item: schemas.TTSCreate, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.create_tts(db=db, item=item)


@router_tts.put("/{pop_id}", summary="更新一个tts")
@web_try()
@sxtimeit
def update_tts(pop_id: int, item: schemas.TTSUpdate, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.update_tts(db, pop_id, item)


@router_tts.get("", summary="获取全部tts列表")
@web_try()
@sxtimeit
def get_tts(params: Params = Depends(), db: Session = Depends(get_db), user=Depends(check_user)):
    return paginate(crud.get_all_tts(db), params)


@router_tts.get("/{blueprint_id}", summary="获取蓝图的tts详情")
@web_try()
@sxtimeit
def get_tts_blueprint(blueprint_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.get_all_tts_blueprint(db, blueprint_id)


@router_tts.delete("/{tts_id}", summary="删除tts")
@web_try()
@sxtimeit
def delete_tts(tts_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.delete_tts(db, tts_id)
