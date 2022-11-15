from fastapi import APIRouter, Depends
from fastapi_pagination import paginate, Params
from sqlalchemy.orm import Session

from app import schemas, get_db, crud
from utils import web_try, sxtimeit

router_customer = APIRouter(
    prefix="/customer",
    tags=["customer-顾客管理"],
)



@router_customer.get("/")
@web_try()
@sxtimeit
def get_customers(params: Params = Depends(), db: Session = Depends(get_db)):
    return paginate(crud.get_customers(db), params)


@router_customer.get("/getOnce/{item_id}")
@web_try()
@sxtimeit
def get_customer_once(item_id: int, db: Session = Depends(get_db)):
    return crud.get_customer_once(db=db, item_id=item_id)


@router_customer.put("/{item_id}")
@web_try()
@sxtimeit
def update_customer(item_id: int, update_item: schemas.CustomerUpdate, db: Session = Depends(get_db)):
    return crud.update_customer(db=db,item_id=item_id,update_item=update_item)


@router_customer.post("/")
@web_try()
@sxtimeit
def add_customer(item: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return crud.create_customer(db=db, item=item)
