from fastapi import APIRouter, Depends
from fastapi_pagination import paginate, Params
from sqlalchemy.orm import Session
from app import schemas, get_db, crud
from utils import web_try, sxtimeit
from app.common.validation import check_user

router_order = APIRouter(
    prefix="/orders",
    tags=["orders-订单管理"],
)


@router_order.get("")
@web_try()
@sxtimeit
def get_orders(params: Params = Depends(), db: Session = Depends(get_db), user=Depends(check_user)):
    return paginate(crud.get_orders(db), params)


@router_order.get("/{order_id}")
@web_try()
@sxtimeit
def get_order_once(update_item: schemas.OrderUpdate, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.get_order_once_dict(db=db, item_id=update_item)


@router_order.put("/{order_id}")
@web_try()
@sxtimeit
def update_order(order_id: int, update_item: schemas.OrderUpdate, db: Session = Depends(get_db),
                 user=Depends(check_user)):
    return crud.update_order(db=db, item_id=order_id, update_item=update_item)


@router_order.delete("/{order_id}")
@web_try()
@sxtimeit
def delete_order(order_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.delete_order(db=db, item_id=order_id)
