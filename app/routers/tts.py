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


@router_tts.post("/store", summary="创建tts")
@web_try()
@sxtimeit
def add_store(item: schemas.TTSCreate, db: Session = Depends(get_db), user=Depends(check_user)):
    item.creator_id = user.id
    return crud.create_store(db=db, item=item)