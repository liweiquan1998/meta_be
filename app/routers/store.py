from fastapi_pagination import paginate, Params
from sqlalchemy.orm import Session
import json
from app import schemas, get_db, crud
from app.common.validation import check_user
from utils import web_try, sxtimeit
from fastapi import Depends
from fastapi import APIRouter
from app.common.validation import *

router_store = APIRouter(
    prefix="/stores",
    tags=["stores-商铺管理"],
)


@router_store.post("/store", summary="创建商铺")
@web_try()
@sxtimeit
def add_store(item: schemas.StoreCreate, db: Session = Depends(get_db), user=Depends(check_user)):
    item.creator_id = user.id
    return crud.create_store(db=db, item=item)


@router_store.delete("/{store_id}", summary="删除商铺")
@web_try()
@sxtimeit
def delete_store(store_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.delete_store(item_id=store_id, db=db)


@router_store.put("/{store_id}", summary="更新商铺信息")
@web_try()
@sxtimeit
def update_store(store_id: int, update_item: schemas.StoreUpdate, db: Session = Depends(get_db), user=Depends(check_user)):
    if json.loads(update_item.sku_ids):
        update_item.sku_ids = json.dumps(list(set(json.loads(update_item.sku_ids))))
    return crud.update_store(db=db, item_id=store_id, update_item=update_item)


@router_store.get("/{store_id}", summary="获取商铺信息")
@web_try()
@sxtimeit
def get_store_once(store_id: int, db: Session = Depends(get_db), user=Depends(check_user) ):
    return crud.get_store_once(db=db, item_id=store_id)


@router_store.get("", summary="获取商铺列表")
@web_try()
@sxtimeit
def get_stores(get_item: schemas.StoreGet = Depends(), params: Params = Depends(), db: Session = Depends(get_db), user=Depends(check_user) ):
    return paginate(crud.get_stores(db, get_item, user), params)


@router_store.get("/{store_id}/blueprint", summary="获取蓝图列表")
@web_try()
@sxtimeit
def get_store_blueprint(store_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.get_blueprint_once_by_store_id(db, store_id)
