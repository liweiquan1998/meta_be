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


@router_businesses.get("/{business}/product_skus/", summary="一个商家下的所有商品类型")  # 正式上线前要记得检验token是否是内部服务
@web_try()
@sxtimeit
def get_businesses_product_skus(business: int, params: schemas.ProductSkuParamsBase = Depends(),
                                db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.get_business_product_skus(db, business, params)


@router_businesses.get("/business/product_skus", summary="一个商家下的所有商品类型")
@web_try()
@sxtimeit
def get_businesses_product_skus(params: schemas.ProductSkuParams = Depends(),
                                db: Session = Depends(get_db), user=Depends(check_user)):
    business_id = user.id
    return paginate(crud.get_business_product_skus(db, business_id, params), params)


@router_businesses.get("/business/orders")
@web_try()
@sxtimeit
def get_business_orders(params:  schemas.BusinessPageParams = Depends(), db: Session = Depends(get_db),
                        user=Depends(check_user)):
    business_id = user.id
    return paginate(crud.get_business_orders(db, business_id, params), params)


@router_businesses.get("/business/after_care")
@web_try()
@sxtimeit
def get_business_except_orders(params: Params = Depends(), db: Session = Depends(get_db), user=Depends(check_user)):
    business_id = user.id
    return paginate(crud.get_business_after_cares(db, business_id), params)


@router_businesses.get("/business/shelves")
@web_try()
@sxtimeit
def get_shelves_once(db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.get_shelves_once_by_creator_id(db=db, creator_id=user.id)


@router_businesses.get("/{business}/blueprints")
@web_try()
@sxtimeit
def get_business_blueprints(business: int, params: Params = Depends(), db: Session = Depends(get_db), user=Depends(check_user)):
    return paginate(crud.get_blueprints_by_creator_id(db, business), params)

