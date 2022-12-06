from fastapi_pagination import paginate, Params
from sqlalchemy.orm import Session

from app import schemas, get_db, crud
from app.common.validation import check_user
from utils import web_try, sxtimeit

from fastapi import Depends
from fastapi import APIRouter
from app.common.validation import *
from app.common.validation import *

router_store = APIRouter(
    prefix="/stores",
    tags=["stores-商铺管理"],
)


@router_store.post("/", summary="创建商铺")
@web_try()
@sxtimeit
def add_store(item: schemas.StoreCreate, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.create_store(db=db, item=item)


@router_store.delete("/{item_id}", summary="删除商铺")
@web_try()
@sxtimeit
def delete_store(item_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.delete_store(item_id=item_id, db=db)


@router_store.put("/{item_id}", summary="更新商铺信息")
@web_try()
@sxtimeit
def update_store(item_id: int, update_item: schemas.StoreUpdate, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.update_store(db=db, item_id=item_id, update_item=update_item)


@router_store.get("/{item_id}", summary="获取商铺信息")
@web_try()
@sxtimeit
def get_store_once(item_id: int, db: Session = Depends(get_db), user=Depends(check_user) ):
    return crud.get_store_once(db=db, item_id=item_id)


@router_store.get("/", summary="获取商铺列表")
@web_try()
@sxtimeit
def get_stores(get_item: schemas.StoreGet = Depends(), params: Params = Depends(), db: Session = Depends(get_db), user=Depends(check_user) ):
    return paginate(crud.get_stores(db, get_item), params)


@router_store.get("/{store_id}/blueprint", summary="获取蓝图列表")
@web_try()
@sxtimeit
def get_store_blueprint(store_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.get_blueprint_once_by_store_id(db, store_id)
