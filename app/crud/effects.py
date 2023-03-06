import time
from sqlalchemy.orm import Session
from app import models


def create_effect(db: Session, item, user):
    # 创建特效
    db_item = models.Effects(**item.dict(), **{'create_time': int(time.time()),
                                               'create_id': user.id,
                                               'status': 0,
                                               })
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_effect(db: Session, user):
    db_query = db.query(models.Effects).filter(models.Effects.create_id == user.id)
    return db_query.order_by(models.Effects.id).all()


def delete_effect(db: Session, item_id):
    # 删除
    item = db.query(models.Effects).filter(models.Effects.id == item_id).first()
    if not item:
        raise Exception(f"effects {item_id} 不存在")
    item.status = 1
    db.commit()
    db.flush()
    db.refresh(item)
    return True
