from fastapi import APIRouter, Depends
from fastapi_pagination import paginate, Params
from sqlalchemy.orm import Session
from app.crud import product
from app import schemas, get_db, crud
from utils import web_try, sxtimeit
from app.common.validation import check_user

router_sku = APIRouter(
    prefix="/skus",
    tags=["skus-库存管理"],
)


@router_sku.get("")
@web_try()
@sxtimeit
def get_skus(params: Params = Depends(), db: Session = Depends(get_db), user=Depends(check_user)):
    return paginate(crud.get_skus(db), params)


@router_sku.get("/{sku_id}")
@web_try()
@sxtimeit
def get_sku_once(sku_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.get_sku_once(db=db, item_id=sku_id)


@router_sku.put("/{sku_id}")
@web_try()
@sxtimeit
def update_sku(sku_id: int, update_item: schemas.SkuUpdate, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.update_sku(db=db, item_id=sku_id, update_item=update_item)


@router_sku.delete("/{sku_id}")
@web_try()
@sxtimeit
def delete_sku(sku_id: int, db: Session = Depends(get_db), user=Depends(check_user)):
    return crud.delete_sku(db=db, item_id=sku_id)


@router_sku.post("/sku")
@web_try()
@sxtimeit
def add_sku(item: schemas.SkuCreate, db: Session = Depends(get_db), user=Depends(check_user)):
    if item.product_id not in [i.id for i in product.get_products(db)]:
        raise Exception(404, "添加失败，要绑定的货物不存在")
    return crud.create_sku(db=db, item=item)
