import time
from app import models, schemas
from sqlalchemy.orm import Session
from app.crud.basic import update_to_db


def create_live_account(db: Session, item: schemas.LiveAccountCreate):
    # sourcery skip: use-named-expression
    # 创建
    db_item = models.LiveAccount(**item.dict(), **{'last_time': int(time.time()),"status": 0})
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_live_account(db: Session, item_id: int, update_item: schemas.LiveAccountUpdate):
    return update_to_db(update_item=update_item, db=db, item_id=item_id, model_cls=models.LiveAccount)


def get_live_account_once(db: Session, item_id: int):
    if item := db.query(models.LiveAccount).filter(models.LiveAccount.id == item_id).first():
        return item
    else:
        raise Exception(f"直播账号id {item_id} 不存在")


def get_live_account_once_by_creator_id(db: Session, creator_id: int):
    if item := db.query(models.LiveAccount).filter(models.LiveAccount.creator_id == creator_id).all():
        return item
    else:
        raise Exception(f"直播账号创建者id {creator_id} 不存在")


def get_live_accounts(db: Session, item: schemas.LiveAccountGet, user):
    name = item.name
    db_query = db.query(models.LiveAccount)
    if user.id:
        db_query = db_query.filter(models.LiveAccount.creator_id == user.id)
    if name:
        search = "%{}%".format(name)
        db_query = db_query.filter(models.LiveAccount.name.like(search))
    return db_query.order_by(-models.LiveAccount.last_time).all()


def get_available_live_accounts(db: Session, item: schemas.LiveAccountGet, user):
    name = item.name
    db_query = db.query(models.LiveAccount)
    if user.id:
        db_query = db_query.filter(models.LiveAccount.status == 0).filter(models.LiveAccount.creator_id == user.id)
    if name:
        search = "%{}%".format(name)
        db_query = db_query.filter(models.LiveAccount.status == 0).filter(models.LiveAccount.name.like(search))
    return db_query.order_by(-models.LiveAccount.last_time).all()


def delete_live_account(db: Session, item_id: int):
    db.query(models.LiveAccount).filter(models.LiveAccount.id == item_id).delete()
    db.commit()
    return True
