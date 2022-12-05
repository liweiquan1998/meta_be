# @author: wanjinhong
# @remarks: sku模块数据库设计为product+sku,目前逻辑为product和sku,所以先临时针对当前业务设计接口
import time
from typing import List,Union
from app import models, schemas
from sqlalchemy.orm import Session
from app.crud.basic import update_to_db
from app.crud.sku import *
from app.crud.product import *
from utils.sx_time import *


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


def update_product_sku(db: Session, item_id: int, update_item: schemas.ProductSkuUpdate):
    product_param, sku_param = split_params(update_item)
    db_sku_item: models.Sku = db.query(models.Sku).filter(models.Sku.id == item_id).first()
    db_sku_item.set_field(sku_param)
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
    sql = '''SELECT  b.*,a.desc,a.meta_obj_id,a.remarks,a.unit,a.business_id
            FROM product a LEFT JOIN sku b ON a.id=b.product_id 
            WHERE b.product_id>0'''
    res: List[models.BaseModel] = db.execute(sql).fetchall()
    return res


def get_business_product_skus(db: Session,business_id, params: Union[schemas.ProductSkuParams,schemas.ProductSkuParamsBase]):
    sql = '''SELECT a.create_time,a.desc,a.meta_obj_id,a.remarks,a.unit,a.business_id,
			b.*,c.thumbnail
            FROM product a LEFT JOIN sku b 
            ON a.id=b.product_id 
            LEFT JOIN meta_obj c ON a.meta_obj_id=c.id 
            where business_id={} AND product_id>0 
            '''
    name_filter_sql = "AND b.sku_name like '%{}%'"
    status_filter_sql = 'AND b.status = {}'
    time_filter_sql = "AND a.create_time>={} AND a.create_time<{}"
    sql = sql.format(business_id)
    if params.name is not None:
        sql += name_filter_sql.format(params.name)
    if params.status is not None:
        sql += status_filter_sql.format(params.status)
    if params.create_time is not None:
        sql += time_filter_sql.format(params.create_time,params.create_time+24*3600)
    rows = db.execute(sql).fetchall()
    res = []
    for row in rows:  # 处理时间戳
        row_buffer = {}
        for field in row.keys():
            data = row[field]
            if 'time' in str(field) and isinstance(data,int):
                data = t2date(data)
            row_buffer.update({field:data})
        res.append(row_buffer)
    return res


def delete_product_sku(db: Session, item_id: int):
    item = get_sku_once(item_id=item_id, db=db)
    if not item:
        raise Exception(f"删除失败, sku  id {item_id}未找到")
    try:
        delete_product(db, item.product_id)
        delete_sku(db, item.id)
    finally:
        db.delete(item)
        db.commit()
        db.flush()
        return True







