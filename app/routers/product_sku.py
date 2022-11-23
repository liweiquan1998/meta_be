from fastapi import APIRouter, Depends
from fastapi_pagination import paginate, Params
from sqlalchemy.orm import Session
from app.crud import product
from app import schemas, get_db, crud
from utils import web_try, sxtimeit
import time

router_product_sku = APIRouter(
    prefix="/product_sku",
    tags=["product_sku-商品库存管理"],
)



@router_product_sku.get("/")
@web_try()
@sxtimeit
def get_product_skus(params: Params = Depends(), db: Session = Depends(get_db)):
    return paginate(crud.get_product_skus(db), params)


@router_product_sku.get("/businesses")
@web_try()
@sxtimeit
def get_businesses_product_skus(business_id, params: Params = Depends(), db: Session = Depends(get_db)):
    return paginate(crud.get_business_product_skus(db,business_id), params)


@router_product_sku.get("/{item_id}")
@web_try()
@sxtimeit
def get_product_sku_once(item_id: int, db: Session = Depends(get_db)):
    return crud.get_product_sku_once_withmeta(db=db, item_id=item_id)


@router_product_sku.put("/{item_id}")
@web_try()
@sxtimeit
def update_product_sku(item_id: int, update_item: schemas.ProductSkuUpdate, db: Session = Depends(get_db)):
    return crud.update_product_sku(db=db,item_id=item_id,update_item=update_item)

@router_product_sku.delete("/{item_id}")
@web_try()
@sxtimeit
def delete_product_sku(item_id: int, db: Session = Depends(get_db)):
    return crud.delete_product_sku(db=db,item_id=item_id)

@router_product_sku.post("/")
@web_try()
@sxtimeit
def add_sku(item: schemas.ProductSkuCreate, db: Session = Depends(get_db)):
    return crud.create_product_sku(db=db, item=item)

