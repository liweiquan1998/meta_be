from fastapi import APIRouter, Depends
from fastapi_pagination import paginate, Params
from sqlalchemy.orm import Session

from app.common.validation import check_user
from app import schemas, get_db, crud
from utils import web_try, sxtimeit
import time


router_apparel = APIRouter(
    prefix="/apparel",
    tags=["apparel-虚拟人服饰管理"],
)


@router_apparel.get("")
@web_try()
@sxtimeit
def get_apparel(params: schemas.ApparelParams = Depends(), db: Session = Depends(get_db), user=Depends(check_user)):
    return paginate(crud.get_apparels(db,params), params)


@router_apparel.get("/{item_id}")
@web_try()
@sxtimeit
def get_apparel_once(item_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.get_apparel_once(db=db, item_id=item_id)


@router_apparel.put("/{item_id}")
@web_try()
@sxtimeit
def update_apparel(item_id: int, update_item: schemas.ApparelUpdate, db: Session = Depends(get_db),
                   user=Depends(check_user)):
    return crud.update_apparel(db=db, item_id=item_id, update_item=update_item)


@router_apparel.delete("/{item_id}")
@web_try()
@sxtimeit
def delete_apparel(item_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.delete_apparel(db=db, item_id=item_id)


@router_apparel.post("/orders/{order_id}")
@web_try()
@sxtimeit
def add_order(item: schemas.ApparelCreate, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.create_apparel(db=db, item=item)


