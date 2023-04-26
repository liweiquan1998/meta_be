import time
from sqlalchemy.orm import Session
from app import models


def create_effect(db: Session, item, user):
    # 创建特效
    db_item = models.Effects(**item.dict(), **{'create_time': int(time.time()),
                                               'creator_id': user.id,
                                               'status': 0,
                                               })
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_effect(db: Session, user, item):
    db_query = db.query(models.Effects).filter(models.Effects.creator_id == user.id)
    db_query = db_query.filter(models.Effects.status == 0)
    if item.name and item.name != "":
        db_query = db_query.filter(models.Effects.name.like(f"%{item.name}%"))
    if item.create_time is not None and item.create_time != -1:
        db_query = db_query.filter(models.Effects.create_time <= item.create_time + 86400)
        db_query = db_query.filter(models.Effects.create_time >= item.create_time)
    return db_query.order_by(-models.Effects.create_time).all()


def delete_effect(db: Session, item_id):
    # 删除
    item = db.query(models.Effects).filter(models.Effects.id == item_id).first()
    if not item:
        raise Exception(f"effects {item_id} 不存在")
    if item.status == 1:
        raise Exception(f"effects {item_id} 已删除")
    item.status = 1
    db.commit()
    db.refresh(item)
    return True
