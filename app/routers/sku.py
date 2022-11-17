from fastapi import APIRouter, Depends
from fastapi_pagination import paginate, Params
from sqlalchemy.orm import Session
from app.crud import product
from app import schemas, get_db, crud
from utils import web_try, sxtimeit
import time

router_sku = APIRouter(
    prefix="/sku",
    tags=["sku-库存管理"],
)



@router_sku.get("/")
@web_try()
@sxtimeit
def get_skus(params: Params = Depends(), db: Session = Depends(get_db)):
    return paginate(crud.get_skus(db), params)


@router_sku.get("/getOnce/{item_id}")
@web_try()
@sxtimeit
def get_sku_once(item_id: int, db: Session = Depends(get_db)):
    return crud.get_sku_once(db=db, item_id=item_id)


@router_sku.put("/{item_id}")
@web_try()
@sxtimeit
def update_sku(item_id: int, update_item: schemas.SkuUpdate, db: Session = Depends(get_db)):
    return crud.update_sku(db=db,item_id=item_id,update_item=update_item)

@router_sku.delete("/{item_id}")
@web_try()
@sxtimeit
def delete_sku(item_id: int, db: Session = Depends(get_db)):
    return crud.delete_sku(db=db,item_id=item_id)

@router_sku.post("/")
@web_try()
@sxtimeit
def add_sku(item: schemas.SkuCreate, db: Session = Depends(get_db)):
    if item.product_id not in [i.id for i in product.get_products(db)]:
        raise Exception(422,"添加失败，要绑定的货物不存在")
    return crud.create_sku(db=db, item=item)

