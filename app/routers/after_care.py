from fastapi import APIRouter, Depends
from fastapi_pagination import paginate, Params
from sqlalchemy.orm import Session

from app.common.validation import check_user
from app import schemas, get_db, crud
from utils import web_try, sxtimeit
import time


router_after_care = APIRouter(
    prefix="/after_care",
    tags=["after_care-售后管理"],
)



@router_after_care.get("")
@web_try()
@sxtimeit
def get_orders(params: Params = Depends(), db: Session = Depends(get_db), user=Depends(check_user)):
    return paginate(crud.get_orders(db), params)


@router_after_care.get("/{item_id}")
@web_try()
@sxtimeit
def get_except_order_once(item_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.get_after_care_once_dict(db=db, item_id=item_id)


@router_after_care.put("/{item_id}")
@web_try()
@sxtimeit
def update_except_order(item_id: int, update_item: schemas.AfterCareUpdate, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.update_after_care(db=db,item_id=item_id,update_item=update_item)


@router_after_care.delete("/{item_id}")
@web_try()
@sxtimeit
def delete_order(item_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.delete_after_care(db=db,item_id=item_id)


@router_after_care.post("/orders/{order_id}")
@web_try()
@sxtimeit
def add_order(item: schemas.AfterCareCreate,order_id:int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.create_after_care(db=db, item=item,order_id=order_id)


