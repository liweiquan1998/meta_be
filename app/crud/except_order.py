import json
import time
from typing import List
from app import models, schemas
from sqlalchemy.orm import Session
from app.crud.basic import update_to_db
from app.crud import order


def create_except_order(db: Session,order_id:int, item: schemas.ExceptOrderCreate):
    db_item = models.ExceptOrder(**item.dict())
    db_item.create_time = time.time()
    db_item.status = 0
    order_item = order.get_order_once(db,order_id)
    if not order_item:
        raise Exception(404,'创建服务失败，找不到原订单')
    if order_item.except_id:
        raise Exception(422,'已经创建过异常服务，不可重复')
    db_item.order_id = order_item.id
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    order_item.except_id = db_item.id
    db.commit()
    db.flush()
    return db_item


def update_except_order(db: Session, item_id: int, update_item: schemas.ExceptOrderUpdate):
    return update_to_db(update_item=update_item, item_id=item_id, db=db, model_cls=models.ExceptOrder)

def get_except_order_once(db: Session, item_id: int):
    res: models.ExceptOrder = db.query(models.ExceptOrder).filter(models.ExceptOrder.id == item_id).first()
    return res

def get_except_order_once_(db: Session, item_id: int) -> dict:
    res: models.ExceptOrder = db.query(models.ExceptOrder).filter(models.ExceptOrder.id == item_id).first()
    if not res:
        return {}
    res_dict = res.to_dict()
    ori_order = order.get_order_once(db, res.order_id)
    if ori_order:
        res_dict.update({'receiver_phone':ori_order.receiver_phone,
                         'receiver_name':ori_order.receiver_name})
    return res_dict

def get_except_orders(db: Session):
    res: List[models.ExceptOrder] = db.query(models.ExceptOrder).all()
    return res

def get_business_except_orders(db: Session,business_id:int):
    res: List[models.ExceptOrder] = db.query(models.ExceptOrder).filter(models.ExceptOrder.business_id == business_id).all()
    return res

def get_customer_except_orders(db: Session,customer_id:int):
    res: List[models.ExceptOrder] = db.query(models.ExceptOrder).filter(models.ExceptOrder.customer_id == customer_id).all()
    return res

def delete_except_order(db: Session, item_id: int):
    item = get_except_order_once(item_id=item_id, db=db)
    if not item:
        raise Exception(f"delete failed, order {item_id} not found")
    db.delete(item)
    db.commit()
    db.flush()

def business_handle_except_order(db:Session,item_id:int,update_item:schemas.BusinessExceptOrderUpdate):
    item = get_except_order_once(item_id=item_id, db=db)
    if not item:
        raise Exception(f"delete failed, order {item_id} not found")
    if item.status != 0:
        raise Exception(403,'退货已经确认或者拒绝，不可重复提交')
    return update_to_db(update_item=update_item, item_id=item_id, db=db, model_cls=models.ExceptOrder)



