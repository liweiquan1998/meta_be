from fastapi import APIRouter, Depends
from fastapi_pagination import paginate, Params
from sqlalchemy.orm import Session

from app.common.validation import check_user
from app.crud import product
from app import schemas, get_db, crud
from utils import web_try, sxtimeit
import time

router_product_sku = APIRouter(
    prefix="/product_skus",
    tags=["product_skus-商品库存管理"],
)


@router_product_sku.get("", summary="分页获取pro_sku或者全量获取")
@web_try()
@sxtimeit
def get_product_skus(total: int = 0, params: Params = Depends(), db: Session = Depends(get_db),
                     user=Depends(check_user)):
    if total:
        return crud.get_product_skus(db)
    return paginate(crud.get_product_skus(db), params)


@router_product_sku.get("/{product_sku_id}")
@web_try()
@sxtimeit
def get_product_sku_once(product_sku_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.get_product_sku_once_withmeta(db=db, item_id=product_sku_id)


@router_product_sku.put("/{product_sku_id}")
@web_try()
@sxtimeit
def update_product_sku(product_sku_id: int, update_item: schemas.ProductSkuUpdate, db: Session = Depends(get_db),
                       user=Depends(check_user)):
    update_item.business_id = user.id
    return crud.update_product_sku(db=db, item_id=product_sku_id, update_item=update_item)


@router_product_sku.delete("/{product_sku_id}")
@web_try()
@sxtimeit
def delete_product_sku(product_sku_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.delete_product_sku(db=db, item_id=product_sku_id)


@router_product_sku.post("/product_sku")
@web_try()
@sxtimeit
def add_sku(item: schemas.ProductSkuCreate, db: Session = Depends(get_db), user=Depends(check_user)):
    business_id = user.id
    return crud.create_product_sku(db=db, item=item, business_id=business_id)
