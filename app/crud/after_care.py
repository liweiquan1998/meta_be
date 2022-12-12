import json
import time
from typing import List
from app import models, schemas
from sqlalchemy.orm import Session
from app.crud.basic import update_to_db
from app.crud import order


def create_after_care(db: Session,order_id:int, item: schemas.AfterCareCreate):
    db_item = models.AfterCare(**item.dict())
    db_item.create_time = time.time()
    db_item.status = 0
    order_item = order.get_order_once(db,order_id)
    if not order_item:
        raise Exception(407,'创建服务失败，找不到原订单')
    if order_item.after_care_id:
        raise Exception(405,'已经创建过异常服务，不可重复')
    db_item.order_id = order_item.id
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    order_item.after_care_id = db_item.id
    db.commit()
    db.flush()
    return db_item


def update_after_care(db: Session, item_id: int, update_item: schemas.AfterCareUpdate):
    return update_to_db(update_item=update_item, item_id=item_id, db=db, model_cls=models.AfterCare)

def get_after_care_once(db: Session, item_id: int):
    res: models.AfterCare = db.query(models.AfterCare).filter(models.AfterCare.id == item_id).first()
    return res

def get_after_care_once_dict(db: Session, item_id: int) -> dict:
    res: models.AfterCare = db.query(models.AfterCare).filter(models.AfterCare.id == item_id).first()
    if not res:
        return {}
    res_dict = res.to_dict()
    ori_order = order.get_order_once(db, res.order_id)
    if ori_order:
        res_dict.update({'receiver_phone':ori_order.receiver_phone,
                         'receiver_name':ori_order.receiver_name})
    return res_dict


def get_after_cares(db: Session):
    res: List[models.AfterCare] = db.query(models.AfterCare).all()
    return res


def get_business_after_cares(db: Session,business_id:int):
    res: List[models.AfterCare] = db.query(models.AfterCare).filter(models.AfterCare.business_id == business_id).all()
    return res


def delete_after_care(db: Session, item_id: int):
    item = get_after_care_once(item_id=item_id, db=db)
    if not item:
        raise Exception(f"delete failed, order {item_id} not found")
    db.delete(item)
    db.commit()
    db.flush()




