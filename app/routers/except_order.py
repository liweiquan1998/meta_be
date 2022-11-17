from fastapi import APIRouter, Depends
from fastapi_pagination import paginate, Params
from sqlalchemy.orm import Session
from app.crud import product
from app import schemas, get_db, crud
from utils import web_try, sxtimeit
import time
from app.handler import order

router_except_order = APIRouter(
    prefix="/except_order",
    tags=["except_order-异常服务单管理"],
)



@router_except_order.get("/")
@web_try()
@sxtimeit
def get_orders(params: Params = Depends(), db: Session = Depends(get_db)):
    return paginate(crud.get_orders(db), params)

@router_order.get("/businesses/{business_id}")
@web_try()
@sxtimeit
def get_business_orders(business_id:int,params: Params = Depends(), db: Session = Depends(get_db)):
    return paginate(crud.get_business_orders(db,business_id), params)

@router_order.get("/customer/{customer_id}")
@web_try()
@sxtimeit
def get_customer_orders(customer_id:int,params: Params = Depends(), db: Session = Depends(get_db)):
    return paginate(crud.get_customer_orders(db,customer_id), params)


@router_order.get("/getOnce/{item_id}")
@web_try()
@sxtimeit
def get_order_once(item_id: int, db: Session = Depends(get_db)):
    return crud.get_order_once(db=db, item_id=item_id)


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

@router_order.put("/deliver/{item_id}/")
@web_try()
@sxtimeit
def deliver_order(item_id: int,item: schemas.OrderDeliver,db: Session = Depends(get_db)):
    return order.deliver_order(db,item_id,item)
