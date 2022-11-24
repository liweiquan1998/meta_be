from fastapi import APIRouter, Depends
from fastapi_pagination import paginate, Params
from sqlalchemy.orm import Session

from app import schemas, get_db, crud
from utils import web_try, sxtimeit

router_product = APIRouter(
    prefix="/products",
    tags=["products-商品管理"],
)



@router_product.get("/")
@web_try()
@sxtimeit
def get_product(params: Params = Depends(), db: Session = Depends(get_db)):
    return paginate(crud.get_products(db), params)


@router_product.get("/{item_id}")
@web_try()
@sxtimeit
def get_product_once(item_id: int, db: Session = Depends(get_db)):
    return crud.get_product_once(db=db, item_id=item_id)


@router_product.put("/{item_id}")
@web_try()
@sxtimeit
def update_product(item_id: int, update_item: schemas.ProductUpdate, db: Session = Depends(get_db)):
    return crud.update_product(db=db,item_id=item_id,update_item=update_item)

@router_product.delete("/{item_id}")
@web_try()
@sxtimeit
def delete_product(item_id: int, db: Session = Depends(get_db)):
    return crud.delete_product(db=db,item_id=item_id)

@router_product.post("/")
@web_try()
@sxtimeit
def add_product(item: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db=db, item=item)
