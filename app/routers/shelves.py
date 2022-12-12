from fastapi_pagination import paginate, Params
from sqlalchemy.orm import Session

from app import schemas, get_db, crud
from app.common.validation import check_user
from utils import web_try, sxtimeit

from fastapi import Depends
from fastapi import APIRouter
from app.common.validation import *
from app.common.validation import *

router_shelves = APIRouter(
    prefix="/shelves",
    tags=["shelves-货架管理"],
)


@router_shelves.post("/shelf", summary="创建货架")
@web_try()
@sxtimeit
def add_shelves(item: schemas.ShelvesCreate, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.create_shelves(db=db, item=item)


@router_shelves.get("/{shelf_id}", summary="获取货架信息")
@web_try()
@sxtimeit
def get_shelves_once(shelf_id: int, db: Session = Depends(get_db), user=Depends(check_user) ):
    return crud.get_shelves_once(db=db, item_id=shelf_id)


@router_shelves.get("/{creator_id}/creator_id", summary="由创建者id->获取货架信息")  # todo  这个还没弄清前端用没用，准备删
@web_try()
@sxtimeit
def get_shelves_once(creator_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.get_shelves_once_by_creator_id(db=db, creator_id=creator_id)


@router_shelves.get("", summary="获取货架列表")
@web_try()
@sxtimeit
def get_shelves(get_item: schemas.ShelvesGet = Depends(), params: Params = Depends(), db: Session = Depends(get_db), user=Depends(check_user)):
    return paginate(crud.get_shelves(db, get_item), params)


@router_shelves.put("/{shelf_id}", summary="更新货架信息")
@web_try()
@sxtimeit
def update_shelves(shelf_id: int, update_item: schemas.ShelvesUpdate, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.update_shelves(db=db, item_id=shelf_id, update_item=update_item)
