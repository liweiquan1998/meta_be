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


@router_tts.get("", summary="获取全部tts列表")
@web_try()
@sxtimeit
def get_tts(params: Params = Depends(), db: Session = Depends(get_db), user=Depends(check_user)):
    return paginate(crud.get_all_tts(db), params)


@router_tts.delete("/{text_id}", summary="删除tts")
@web_try()
@sxtimeit
def delete_tts(text_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.delete_tts(db, text_id)
