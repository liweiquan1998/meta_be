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
def get_businesses_product_skus(business_id:str,name:str=None,status:int=None,create_time:int=None,
                                params: Params = Depends(), db: Session = Depends(get_db)):
    return paginate(crud.get_business_product_skus(db,int(business_id),name,status,create_time), params)


@router_businesses.get("/{business_id}/orders")
@web_try()
@sxtimeit
def get_business_orders(business_id:str,params: Params = Depends(), db: Session = Depends(get_db)):
    return paginate(crud.get_business_orders(db,schemas.BusinessPageParams(business_id=int(business_id))), params)

@router_businesses.get("/{business_id}/except_orders")
@web_try()
@sxtimeit
def get_business_except_orders(business_id:str,params:Params = Depends(), db: Session = Depends(get_db)):
    return paginate(crud.get_business_except_orders(db,int(business_id)), params)