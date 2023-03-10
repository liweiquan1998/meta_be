import time
from typing import List
from app import models, schemas
from sqlalchemy.orm import Session
from app.crud.basic import update_to_db


def create_blueprint(db: Session, item: schemas.BlueprintCreate):
    if db.query(models.BluePrint).filter(models.BluePrint.store_id == item.store_id).first():
        raise Exception(f"店铺id {item.store_id} 已有保存的蓝图")
    if db.query(models.User).filter(models.User.id == item.creator_id).first() is None:
        raise Exception(f"创建者id {item.creator_id} 不存在")
    if db.query(models.Store).filter(models.Store.id == item.store_id).first() is None:
        raise Exception(f"店铺 {item.store_id} 不存在")
    # 创建
    db_item = models.BluePrint(**item.dict(), **{"create_time": int(time.time())})
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_blueprint(db: Session, item_id: int, update_item: schemas.BlueprintUpdate):
    return update_to_db(update_item=update_item, item_id=item_id, db=db, model_cls=models.BluePrint)


def get_blueprint_once(db: Session, item_id: int):
    res: models.BluePrint = db.query(models.BluePrint).filter(models.BluePrint.id == item_id).first()
    return res


def get_blueprint_once_by_store_id(db: Session, item_id: int):
    res: models.BluePrint = db.query(models.BluePrint).filter(models.BluePrint.store_id == item_id).first()
    return res


def get_blueprints_by_creator_id(db: Session, user_id):
    blueprints: List[models.BluePrint] = db.query(models.BluePrint).filter(models.BluePrint.creator_id == user_id).all()
    return blueprints


def get_blueprints(db: Session):
    blueprints: List[models.BluePrint] = db.query(models.BluePrint).all()
    return blueprints


def delete_blueprint(db: Session, item_id: int):
    db.query(models.BluePrint).filter(models.BluePrint.id == item_id).delete()
    db.commit()
    return True
