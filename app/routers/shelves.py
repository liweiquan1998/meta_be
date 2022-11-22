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


@router_shelves.post("/create", summary="创建货架")
@web_try()
@sxtimeit
def add_shelves(item: schemas.ShelvesCreate, db: Session = Depends(get_db)):
    return crud.create_shelves(db=db, item=item)


@router_shelves.get("/{item_id}", summary="获取货架信息")
@web_try()
@sxtimeit
def get_shelves_once(item_id: int, db: Session = Depends(get_db), ):
    return crud.get_shelves_once(db=db, item_id=item_id)


@router_shelves.get("/", summary="获取货架列表")
@web_try()
@sxtimeit
def get_shelves(get_item: schemas.ShelvesGet = Depends(), params: Params = Depends(), db: Session = Depends(get_db), ):
    return paginate(crud.get_shelves(db, get_item), params)


@router_shelves.put("/{item_id}", summary="更新货架信息")
@web_try()
@sxtimeit
def update_shelves(item_id: int, update_item: schemas.ShelvesUpdate, db: Session = Depends(get_db)):
    return crud.update_shelves(db=db, item_id=item_id, update_item=update_item)
