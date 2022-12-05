from fastapi_pagination import paginate, Params
from sqlalchemy.orm import Session

from app import schemas, get_db, crud
from app.common.validation import check_user
from utils import web_try, sxtimeit

from fastapi import Depends
from fastapi import APIRouter
from app.common.validation import *
from app.common.validation import *

router_live_account = APIRouter(
    prefix="/live_account",
    tags=["live_account-直播账号管理"],
)


@router_live_account.post("", summary="创建直播账号")
@web_try()
@sxtimeit
def add_live_account(item: schemas.LiveAccountCreate, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.create_live_account(db=db, item=item)


@router_live_account.get("/{item_id}", summary="获取直播账号信息")
@web_try()
@sxtimeit
def get_live_account_once(item_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.get_live_account_once(db=db, item_id=item_id)


@router_live_account.get("/{creator_id}/creator_id", summary="由创建者id->获取直播账号信息")
@web_try()
@sxtimeit
def get_live_account_once(creator_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.get_live_account_once_by_creator_id(db=db, creator_id=creator_id)


@router_live_account.get("", summary="获取直播账号列表")
@web_try()
@sxtimeit
def get_live_account(get_item: schemas.LiveAccountGet = Depends(), params: Params = Depends(),
                     db: Session = Depends(get_db), user=Depends(check_user) ):
    return paginate(crud.get_live_accounts(db, get_item), params)


@router_live_account.put("/{item_id}", summary="更新直播账号信息")
@web_try()
@sxtimeit
def update_live_account(item_id: int, update_item: schemas.LiveAccountUpdate, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.update_live_account(db=db, item_id=item_id, update_item=update_item)


@router_live_account.delete("/{item_id}", summary="删除直播账号")
@web_try()
@sxtimeit
def delete_live_account(item_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.delete_live_account(db=db, item_id=item_id)
