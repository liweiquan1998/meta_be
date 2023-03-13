import time
from app import models, schemas
from sqlalchemy.orm import Session
from app.crud.basic import update_to_db


def create_background(db: Session, item: schemas.BackgroundCreate):
    # sourcery skip: use-named-expression
    # 重复名称判断
    # 创建
    db_item = models.Background(**item.dict(), **{'create_time': int(time.time())})
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_background(db: Session, item_id: int, update_item: schemas.BackgroundUpdate):
    return update_to_db(update_item=update_item, db=db, item_id=item_id, model_cls=models.Background)


def get_background_once(db: Session, item_id: int):
    if item := db.query(models.Background).filter(models.Background.id == item_id).first():
        return item
    else:
        raise Exception(f"背景id {item_id} 不存在")


def get_backgrounds(db: Session, item: schemas.BackgroundGet):
    db_query = db.query(models.Background)
    if item.name:
        db_query = db_query.filter(models.Background.name.like(f"%{item.name}%"))
    if item.type is not None:
        db_query = db_query.filter(models.Background.type == item.type)
    return db_query.order_by(models.Background.id).all()


def delete_background(db: Session, item_id: int):
    db.query(models.Background).filter(models.Background.id == item_id).delete()
    db.commit()
    return True
