import time
from typing import List
from app import models, schemas
from sqlalchemy.orm import Session
from app.crud.basic import update_to_db
from app.common.validation import *


def create_store(db: Session, item: schemas.StoreCreate):
    # sourcery skip: use-named-expression
    # 重复店铺名检查
    if db.query(models.Store).filter(models.Store.name == item.name).first():
        raise Exception(f"店铺名 {item.name} 已存在")
    if db.query(models.Scene).filter(models.Scene.id == item.scene_id).first() is None:
        raise Exception(f"场景id {item.scene_id} 不存在")
    if db.query(models.User).filter(models.User.id == item.creator_id).first() is None:
        raise Exception(f"创建者id {item.creator_id} 不存在")
    # 创建
    db_item = models.Store(**item.dict(), **{"create_time": int(time.time())})
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_store(db: Session, item_id: int, update_item: schemas.StoreUpdate):
    return update_to_db(update_item=update_item, item_id=item_id, db=db, model_cls=models.Store)


def get_store_once(db: Session, item_id: int):
    res: models.Store = db.query(models.Store).filter(models.Store.id == item_id).first()
    return res


def get_stores(db: Session, item: schemas.StoreGet):
    db_query = db.query(models.Store)
    if item.name:
        db_query = db_query.filter(models.Store.name.like(f"%{item.name}%"))
    return db_query.all()

def delete_store(db: Session, item_id: int):
    db.query(models.Store).filter(models.Store.id == item_id).delete()
    db.commit()
    return f'删除店铺 {item_id} 成功'