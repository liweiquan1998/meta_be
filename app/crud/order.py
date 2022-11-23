import json
import time
from typing import List
from app import models, schemas
from sqlalchemy.orm import Session
from app.crud.basic import update_to_db
from app.crud.product_sku import *

def create_order(db: Session, item: schemas.OrderCreate):
    db_item = models.Order(**item.dict())
    db_item.create_time = time.time()
    db_item.status = 0
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_order(db: Session, item_id: int, update_item: schemas.OrderUpdate):
    return update_to_db(update_item=update_item, item_id=item_id, db=db, model_cls=models.Order)

def get_order_once(db: Session, item_id: int):
    res: models.Order = db.query(models.Order).filter(models.Order.id == item_id).first()
    return res

def get_order_once_dict(db:Session, item_id:int):
    res: models.Order = db.query(models.Order).filter(models.Order.id == item_id).first()
    res_dict:dict = res.to_dict()
    res_dict['sku_snapshot'] = json.loads(res_dict.get('sku_snapshot','{}'))
    res_dict['except_order'] = db.query(models.ExceptOrder).filter(models.ExceptOrder.id == res.except_id).first()
    return res_dict


def get_orders(db: Session):
    res: List[models.Order] = db.query(models.Order).all()
    return res

def get_business_orders(db: Session, business_id:int):
    res: List[models.Order] = db.query(models.Order).filter(models.Order.business_id == business_id).all()
    return res

def get_customer_orders(db: Session, customer_id:int):
    res: List[models.Order] = db.query(models.Order).filter(models.Order.customer_id == customer_id).all()
    return res

def delete_order(db: Session, item_id: int):
    item = get_order_once(item_id=item_id, db=db)
    if not item:
        raise Exception(f"delete failed, order {item_id} not found")
    db.delete(item)
    db.commit()
    db.flush()