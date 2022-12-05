from fastapi import APIRouter, Depends
from fastapi_pagination import paginate, Params
from sqlalchemy.orm import Session
from app import schemas, get_db, crud
from app.common.validation import check_user
from utils import web_try, sxtimeit

router_businesses = APIRouter(
    prefix="/businesses",
    tags=["businesses-商家管理"],
)


@router_businesses.get("/{business_id}/product_skus", summary="一个商家下的所有商品类型")
@web_try()
@sxtimeit
def get_businesses_product_skus(business_id: str, name: str = None, status: int = None, create_time: int = None,
                                params: Params = Depends(), db: Session = Depends(get_db), user=Depends(check_user)):
    return paginate(crud.get_business_product_skus(db, int(business_id), name, status, create_time), params)


@router_businesses.get("/business/orders")
@web_try()
@sxtimeit
def get_business_orders(params:  schemas.BusinessPageParams = Depends(), db: Session = Depends(get_db),
                        user=Depends(check_user)):
    business_id = user.id
    return paginate(crud.get_business_orders(db, business_id,
                                             schemas.BusinessPageParams(business_id=int(business_id))), params)


@router_businesses.get("/{business_id}/after_care")
@web_try()
@sxtimeit
def get_business_except_orders(business_id: str, params: Params = Depends(), db: Session = Depends(get_db), user=Depends(check_user)):
    return paginate(crud.get_business_after_cares(db, int(business_id)), params)