# @author: wanjinhong
# @remarks: sku模块数据库设计为product+sku,目前逻辑为product和sku,所以先临时针对当前业务设计接口
import json
import time
from typing import Union, List
from app import models, schemas
from sqlalchemy.orm import Session
from app.crud.sku import delete_sku, get_sku_once
from app.crud.product import delete_product
from utils.sx_time import t2date


def split_params(item: schemas.ProductSkuBase):
    product_params = ['desc', 'unit', 'remarks', 'meta_obj_id', 'business_id']
    product, sku = dict(), dict()
    for key, value in item.dict().items():
        if key in product_params:
            product[key] = value
        else:
            sku[key] = value
    return product, sku


def create_product_sku(db: Session, item: schemas.ProductSkuCreate,business_id:int):
    product_param, sku_param = split_params(item)
    sku_name = sku_param['sku_name']
    res = db.query(models.Sku).filter(models.Sku.sku_name == sku_name).first()
    if res:
        raise Exception(f'商品名称 {sku_name} 重复')
    db_product_item = models.Product(**product_param)
    db_product_item.create_time = time.time()
    db_product_item.business_id = business_id
    db.add(db_product_item)
    db.commit()
    db.refresh(db_product_item)
    db_sku_item = models.Sku(**sku_param)
    db_sku_item.status = 1
    db_sku_item.product_id = db_product_item.id
    db.add(db_sku_item)
    db.commit()
    db.refresh(db_sku_item)
    res: dict = db_product_item.to_dict()
    res.update(db_sku_item.to_dict())
    return res

# 获取上架sku_ids
def get_product_sku_once(db: Session, creator_id: int):
    store_list: List[models.Store] = db.query(models.Store).filter(
        models.Store.creator_id == creator_id).all()
    shelf_ids = []
    for store_item in store_list:
        if store_item.sku_ids:
            sku_ids = json.loads(store_item.sku_ids)
            shelf_ids.extend([sku_info['shelf_id'] for sku_info in sku_ids])
    return shelf_ids

def update_product_sku(db: Session, item_id: int, update_item: schemas.ProductSkuUpdate):
    product_param, sku_param = split_params(update_item)
    db_sku_item: models.Sku = db.query(models.Sku).filter(models.Sku.id == item_id).first()
    if not db_sku_item:
        raise Exception(400, '商品不存在')
    sku_item_original_status = db_sku_item.status
    db_sku_item.set_field(sku_param)
    if sku_item_original_status == 1 and db_sku_item.status == 0:  # 下架某个商品
        shelf_ids = get_product_sku_once(db, update_item.business_id)
        if db_sku_item.id in shelf_ids:
            raise Exception(400, '该商品已经被上货架，不可以直接下架')
    db_product_item: models.Product = db.query(models.Product).filter(
        models.Product.id == db_sku_item.product_id).first()
    db_product_item.set_field(product_param)
    db_product_item.last_update = time.time()
    db.commit()
    db.flush()
    res: dict = db_product_item.to_dict()
    res.update(db_sku_item.to_dict())
    return res


def get_product_sku_once(db: Session, item_id: int):
    res: models.Sku = db.query(models.Sku).filter(models.Sku.id == item_id).first()
    if res:
        product_res: models.Product = db.query(models.Product).filter(models.Product.id == res.product_id).first()
        res = res.to_dict()
        sku_res = product_res.to_dict()
        sku_res.pop('id')
        res.update(sku_res)
    return res


def get_product_sku_once_withmeta(db: Session, item_id: int):
    res: models.Sku = db.query(models.Sku).filter(models.Sku.id == item_id).first()
    if res:
        product_res: models.Product = db.query(models.Product).filter(models.Product.id == res.product_id).first()
        res:dict = res.to_dict()
        sku_res = product_res.to_dict()
        sku_res.pop('id')
        res.update(sku_res)
        meta: models.MetaObj = db.query(models.MetaObj).filter(models.MetaObj.id == res.get("meta_obj_id")).first()
        res['meta_obj'] = meta.to_dict() if meta else None
    return res


def get_product_skus(db: Session):
    res = db.query(models.Product,
                   models.Sku).join(models.Sku,
                                    models.Product.id == models.Sku.product_id,
                                    isouter=True).filter(models.Sku.product_id > 0).all()

    def combine(item):
        row = item.Product.to_dict()
        row.update(item.Sku.to_dict())
        return row

    res = list(map(combine, res))
    return res


def get_business_product_skus(db: Session, business_id, params: Union[schemas.ProductSkuParams,schemas.ProductSkuParamsBase]):
    query = db.query(models.Sku, models.Product, models.MetaObj). \
        join(models.MetaObj, models.Product.meta_obj_id == models.MetaObj.id). \
        join(models.Sku, models.Product.id == models.Sku.product_id, isouter=True). \
        filter(models.Product.business_id == business_id, models.Sku.product_id > 0)
    if params.name is not None:
        query = query.filter(models.Sku.sku_name.like(f'%{params.name}%'))
    if params.status is not None:
        query = query.filter(models.Sku.status == params.status)
    if params.create_time is not None:
        query = query.filter(models.Product.create_time >= params.create_time,
                             models.Product.create_time < params.create_time + 24 * 3600)
    rows = query.order_by(-models.Product.create_time).all()
    res = []

    def combine(item):
        row: dict = item.MetaObj.to_dict()
        row.update(item.Product.to_dict())
        row.update(item.Sku.to_dict())
        return row

    rows = list(map(combine, rows))
    for row in rows:  # 处理时间戳and添加metaobj
        row_buffer = {}
        for field in row.keys():
            data = row[field]
            if 'time' in str(field) and isinstance(data, int):
                data = t2date(data)
            row_buffer.update({field: data})
        res.append(row_buffer)
    return res


def delete_product_sku(db: Session, item_id: int):
    item = get_sku_once(item_id=item_id, db=db)
    if not item:
        raise Exception(f"删除失败, sku  id {item_id}未找到")
    if item.status == 1:
        raise Exception(f"该商品已经被上架，不可以直接删除")
    try:
        delete_product(db, item.product_id)
        delete_sku(db, item.id)
    finally:
        db.delete(item)
        db.commit()
        db.flush()
        return True
