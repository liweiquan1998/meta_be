from fastapi import APIRouter, Depends
from fastapi_pagination import paginate, Params
from sqlalchemy.orm import Session

from app.common.validation import check_user
from app.crud import product
from app import schemas, get_db, crud
from utils import web_try, sxtimeit
import time

router_product_sku = APIRouter(
    prefix="/product_sku",
    tags=["product_sku-商品库存管理"],
)



@router_product_sku.get("/",summary="分页获取pro_sku或者全量获取")
@web_try()
@sxtimeit
def get_product_skus(total: int = 0, params: Params = Depends(), db: Session = Depends(get_db), user=Depends(check_user)):
    if total:
        return crud.get_product_skus(db)
    return paginate(crud.get_product_skus(db), params)


@router_product_sku.get("/{item_id}")
@web_try()
@sxtimeit
def get_product_sku_once(item_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.get_product_sku_once_withmeta(db=db, item_id=item_id)


@router_product_sku.put("/{item_id}")
@web_try()
@sxtimeit
def update_product_sku(item_id: int, update_item: schemas.ProductSkuUpdate, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.update_product_sku(db=db,item_id=item_id,update_item=update_item)

@router_product_sku.delete("/{item_id}")
@web_try()
@sxtimeit
def delete_product_sku(item_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.delete_product_sku(db=db,item_id=item_id)

@router_product_sku.post("/")
@web_try()
@sxtimeit
def add_sku(item: schemas.ProductSkuCreate, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.create_product_sku(db=db, item=item)

