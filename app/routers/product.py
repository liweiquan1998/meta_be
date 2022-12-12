from fastapi import APIRouter, Depends
from fastapi_pagination import paginate, Params
from sqlalchemy.orm import Session

from app import schemas, get_db, crud
from utils import web_try, sxtimeit
from app.common.validation import *

router_product = APIRouter(
    prefix="/products",
    tags=["products-商品管理"],
)


@router_product.get("/")
@web_try()
@sxtimeit
def get_product(params: Params = Depends(), db: Session = Depends(get_db), user=Depends(check_user)):
    return paginate(crud.get_products(db), params)


@router_product.get("/{product_id}")
@web_try()
@sxtimeit
def get_product_once(product_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.get_product_once(db=db, item_id=product_id)


@router_product.put("/{product_id}")
@web_try()
@sxtimeit
def update_product(product_id: int, update_item: schemas.ProductUpdate, db: Session = Depends(get_db),
                   user=Depends(check_user)):
    return crud.update_product(db=db, item_id=product_id, update_item=update_item)


@router_product.delete("/{item_id}")
@web_try()
@sxtimeit
def delete_product(item_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.delete_product(db=db, item_id=item_id)


@router_product.post("/product")
@web_try()
@sxtimeit
def add_product(item: schemas.ProductCreate, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.create_product(db=db, item=item)
