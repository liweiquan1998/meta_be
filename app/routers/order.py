from fastapi import APIRouter, Depends
from fastapi_pagination import paginate, Params
from sqlalchemy.orm import Session
from app.crud import product
from app import schemas, get_db, crud
from utils import web_try, sxtimeit
import time
from app.handler import order

router_order = APIRouter(
    prefix="/order",
    tags=["order-订单管理"],
)



@router_order.get("/")
@web_try()
@sxtimeit
def get_orders(params: Params = Depends(), db: Session = Depends(get_db)):
    return paginate(crud.get_orders(db), params)

@router_order.get("/businesses")
@web_try()
@sxtimeit
def get_business_orders(params: schemas.BusinessPageParams = Depends(), db: Session = Depends(get_db)):
    return paginate(crud.get_business_orders(db,params), params)


@router_order.get("/{item_id}")
@web_try()
@sxtimeit
def get_order_once(item_id: int, db: Session = Depends(get_db)):
    return crud.get_order_once_dict(db=db, item_id=item_id)


@router_order.put("/{item_id}")
@web_try()
@sxtimeit
def update_order(item_id: int, update_item: schemas.OrderUpdate, db: Session = Depends(get_db)):
    return crud.update_order(db=db,item_id=item_id,update_item=update_item)

@router_order.delete("/{item_id}")
@web_try()
@sxtimeit
def delete_order(item_id: int, db: Session = Depends(get_db)):
    return crud.delete_order(db=db,item_id=item_id)

@router_order.post("/")
@web_try()
@sxtimeit
def add_order(item: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db=db, item=item)


@router_order.put("/{item_id}/deliver_status")
@web_try()
@sxtimeit
def deliver_order(item_id: int,item: schemas.OrderDeliver,db: Session = Depends(get_db)):
    return order.deliver_order(db,item_id,item)

@router_order.put("/{item_id}/except_status")
@web_try()
@sxtimeit
def except_order(item_id: int,item: schemas.OrderExcept,db: Session = Depends(get_db)):
    return order.except_order(db,item_id,item)
