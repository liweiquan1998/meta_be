from fastapi_pagination import paginate, Params
from sqlalchemy.orm import Session

from app import schemas, get_db, crud
from app.common.validation import check_user
from utils import web_try, sxtimeit

from fastapi import Depends
from fastapi import APIRouter
from app.common.validation import *
from app.common.validation import *

router_virtual_humans = APIRouter(
    prefix="/virtual_humans",
    tags=["virtual_humans-虚拟人管理"],
)


@router_virtual_humans.post("/", summary="创建虚拟人")
@web_try()
@sxtimeit
def add_virtual_human(item: schemas.VirtualHumanCreate, db: Session = Depends(get_db)):
    return crud.create_virtual_human(db=db, item=item)


@router_virtual_humans.delete("/{item_id}", summary="删除虚拟人")
@web_try()
@sxtimeit
def delete_virtual_human(item_id: int, db: Session = Depends(get_db)):
    return crud.delete_virtual_human(item_id=item_id, db=db)


@router_virtual_humans.put("/{item_id}", summary="更新虚拟人信息")
@web_try()
@sxtimeit
def update_virtual_human(item_id: int, update_item: schemas.VirtualHumanUpdate, db: Session = Depends(get_db)):
    return crud.update_virtual_human(db=db, item_id=item_id, update_item=update_item)


@router_virtual_humans.get("/", summary="获取虚拟人列表")
@web_try()
@sxtimeit
def get_virtual_humans(get_item: schemas.VirtualHumanGet = Depends(), params: Params = Depends(),
                       db: Session = Depends(get_db)):
    return paginate(crud.get_virtual_humans(db, get_item), params)


@router_virtual_humans.get("/{item_id}", summary="获取虚拟人信息")
@web_try()
@sxtimeit
def get_virtual_human_once(item_id: int, db: Session = Depends(get_db)):
    return crud.get_virtual_human_once(db=db, item_id=item_id)

