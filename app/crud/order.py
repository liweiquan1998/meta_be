import json
import time
from typing import List

from app import models, schemas
from sqlalchemy.orm import Session
from utils import t2date, trans_t2date


def create_order(db: Session, item: schemas.OrderCreate):
    db_item = models.Order(**item.dict())
    db_item.create_time = time.time()
    db_item.status = 0
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_order(db: Session, item_id: int, update_item: schemas.OrderUpdate):
    order_db_item: models.Order = db.query(models.Order).filter(models.Order.id == item_id).first()
    original_status = order_db_item.status
    order_db_item.set_field(update_item.dict())
    after_care = after_care_db_item = False
    if original_status == -1 and order_db_item.status == 3:  # 商家确认退款
        after_care = True
        after_care_db_item: models.AfterCare = db.query(models.AfterCare).\
                            filter(models.AfterCare.id == order_db_item.after_care_id).first()
        after_care_db_item.set_field(update_item.dict())
        after_care_db_item.status = 1
        order_db_item.close_time = time.time()
    db.commit()
    db.refresh(order_db_item)
    if after_care:
        db.refresh(after_care_db_item)
    return order_db_item


def get_order_once(db: Session, item_id: int):
    res: models.Order = db.query(models.Order).filter(models.Order.id == item_id).first()
    return res


def get_order_once_dict(db: Session, item_id: int):
    res: models.Order = db.query(models.Order).filter(models.Order.id == item_id).first()
    if res.create_time:
        res.create_time = t2date(res.create_time)
    if res.deliver_time:
        res.deliver_time = t2date(res.deliver_time)
    res_dict:dict = res.to_dict()
    business_info: models.User = db.query(models.User).filter(models.User.id == res.business_id).first()
    res_dict['deliver_name'] = business_info.name if business_info else '商家姓名丢失'
    res_dict['deliver_phone'] = business_info.tel_phone if business_info else '商家电话信息丢失'
    res_dict['sku_snapshot'] = json.loads(res_dict.get('sku_snapshot', '{}'))
    res_dict['except_order'] = db.query(models.AfterCare).filter(models.AfterCare.id == res.after_care_id).first()
    return res_dict


def get_orders(db: Session):
    res: List[models.Order] = db.query(models.Order).order_by(models.Order.create_time.desc()).all()
    return res


def get_business_orders(db: Session, business_id: int, params: schemas.BusinessPageParams):
    query = db.query(models.Order).filter(models.Order.business_id == business_id)
    if params.status is not None:
        query = query.filter(models.Order.status == params.status)
    if params.order_num:
        query = query.filter(models.Order.order_number.like(f'%{params.order_num}%'))
    if params.create_time:
        day_begin = int(params.create_time)
        day_end = day_begin + 3600 * 24
        query = query.filter(models.Order.create_time.between(day_begin, day_end))
    res: List[models.Order] = query.order_by(models.Order.create_time.desc()).all()
    for item in res:
        if item.sku_snapshot:  # sku快照的反序列化和时间戳转字符串
            item.sku_snapshot = json.loads(item.sku_snapshot)
            if item.sku_snapshot.get('create_time'):
                item.sku_snapshot['create_time'] = t2date(item.sku_snapshot['create_time'])
        trans_t2date(item)
    return res


def get_customer_orders(db: Session, customer_id: int):
    res: List[models.Order] = db.query(models.Order).filter(models.Order.customer_id == customer_id).all()
    return res


def delete_order(db: Session, item_id: int):
    item = get_order_once(item_id=item_id, db=db)
    if not item:
        raise Exception(f"delete failed, order {item_id} not found")
    db.delete(item)
    db.commit()
    db.flush()
    return True

