from fastapi_pagination import paginate, Params
from sqlalchemy.orm import Session

from app import schemas, get_db, crud
from app.common.validation import check_user
from utils import web_try, sxtimeit

from fastapi import Depends
from fastapi import APIRouter
from app.common.validation import *
from app.common.validation import *

router_live_streaming = APIRouter(
    prefix="/live_streamings",
    tags=["live_streamings-直播间管理"],
)


@router_live_streaming.post("/live_streaming", summary="创建直播间")
@web_try()
@sxtimeit
def add_live_streaming(item: schemas.LiveStreamingCreate, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.create_live_streaming(db=db, item=item, user=user)


@router_live_streaming.get("/{stream_id}", summary="获取直播间信息")
@web_try()
@sxtimeit
def get_live_streaming_once(stream_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.get_live_streaming_once(db=db, item_id=stream_id)


@router_live_streaming.get("", summary="获取直播间列表")
@web_try()
@sxtimeit
def get_live_streaming(get_item: schemas.LiveStreamingGet = Depends(), params: Params = Depends(),
                       db: Session = Depends(get_db), user=Depends(check_user)):
    return paginate(crud.get_live_streamings(db, get_item, user), params)


@router_live_streaming.put("/{stream_id}", summary="更新直播间信息")
@web_try()
@sxtimeit
def update_live_streaming(stream_id: int, update_item: schemas.LiveStreamingUpdate, db: Session = Depends(get_db),
                          user=Depends(check_user)):
    return crud.update_live_streaming(db=db, item_id=stream_id, update_item=update_item)


@router_live_streaming.delete("/{stream_id}", summary="删除直播间")
@web_try()
@sxtimeit
def delete_live_streaming(stream_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.delete_live_streaming(db=db, item_id=stream_id)
