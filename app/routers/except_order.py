from fastapi import APIRouter, Depends
from fastapi_pagination import paginate, Params
from sqlalchemy.orm import Session
from app.crud import product
from app import schemas, get_db, crud
from utils import web_try, sxtimeit
import time
from app.handler import order

router_except_order = APIRouter(
    prefix="/except_orders",
    tags=["except_orders-异常服务单管理"],
)



@router_except_order.get("/")
@web_try()
@sxtimeit
def get_orders(params: Params = Depends(), db: Session = Depends(get_db)):
    return paginate(crud.get_orders(db), params)

@router_except_order.get("/businesses")
@web_try()
@sxtimeit
def get_business_except_orders(params: schemas.BusinessPageParams = Depends(), db: Session = Depends(get_db)):
    return paginate(crud.get_business_except_orders(db,params.business_id), params)


@router_except_order.get("/{item_id}")
@web_try()
@sxtimeit
def get_except_order_once(item_id: int, db: Session = Depends(get_db)):
    return crud.get_except_order_once_(db=db, item_id=item_id)


@router_except_order.put("/{item_id}")
@web_try()
@sxtimeit
def update_except_order(item_id: int, update_item: schemas.ExceptOrderUpdate, db: Session = Depends(get_db)):
    return crud.update_except_order(db=db,item_id=item_id,update_item=update_item)

@router_except_order.put("/business/{item_id}")
@web_try()
@sxtimeit
def update_business_except_order(item_id: int, update_item: schemas.BusinessExceptOrderUpdate, db: Session = Depends(get_db)):
    return crud.business_handle_except_order(db=db,item_id=item_id,update_item=update_item)

@router_except_order.delete("/{item_id}")
@web_try()
@sxtimeit
def delete_order(item_id: int, db: Session = Depends(get_db)):
    return crud.delete_except_order(db=db,item_id=item_id)

@router_except_order.post("/orders/{order_id}")
@web_try()
@sxtimeit
def add_order(item: schemas.ExceptOrderCreate,order_id:int, db: Session = Depends(get_db)):
    return crud.create_except_order(db=db, item=item,order_id=order_id)

