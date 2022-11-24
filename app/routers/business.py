from fastapi import APIRouter, Depends
from fastapi_pagination import paginate, Params
from sqlalchemy.orm import Session
from app import schemas, get_db, crud
from utils import web_try, sxtimeit

router_businesses = APIRouter(
    prefix="/businesses",
    tags=["businesses-商家管理"],
)


@router_businesses.get("/{business_id}/product_skus",summary="一个商家下的所有商品类型")
@web_try()
@sxtimeit
def get_businesses_product_skus(business:str, params: Params = Depends(), db: Session = Depends(get_db)):
    return paginate(crud.get_business_product_skus(db,int(business)), params)


@router_businesses.get("/{business_id}/orders")
@web_try()
@sxtimeit
def get_business_orders(business:str,params: Params = Depends(), db: Session = Depends(get_db)):
    return paginate(crud.get_business_orders(db,int(business)), params)

@router_businesses.get("/{business_id}/except_orders")
@web_try()
@sxtimeit
def get_business_except_orders(business:str,params:Params = Depends(), db: Session = Depends(get_db)):
    return paginate(crud.get_business_except_orders(db,int(business)), params)