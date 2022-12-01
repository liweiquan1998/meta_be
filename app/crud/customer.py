import time
from typing import List
from app import models, schemas
from sqlalchemy.orm import Session
from app.crud.basic import update_to_db
from app.common.validation import *

def create_customer(db: Session, item: schemas.CustomerCreate):
    # 重复用户名检查
    res: models.Customer = db.query(models.Customer).filter(models.Customer.name == item.name).first()
    if res:
        raise Exception(f"用户 {item.name} 已存在")
    # 创建
    password = item.password
    del item.password
    db_item = models.Customer(**item.dict(),
                              **{'password_hash': get_password_hash(password),
                                 "create_time": int(time.time()),
                                 "update_time": int(time.time()),
                                 "last_login": int(time.time())})
    db_item.auth_token = create_access_token(db_item.name, 'customer')
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# def update_customer(db: Session, item_id: int, update_item: schemas.CustomerUpdate):
#     return update_to_db(update_item=update_item, item_id=item_id, db=db, model_cls=models.Customer)


def get_customer_once(db: Session, item_id: int):
    res: models.Customer = db.query(models.Customer).filter(models.Customer.id == item_id).first()
    return res

def get_customer_once_by_name(db: Session, name: str):
    res: models.Customer = db.query(models.Customer).filter(models.Customer.name == name).first()
    return res


def get_customers(db: Session, item: schemas.CustomerGet):
    db_query = db.query(models.Customer)
    if item.name:
        db_query = db_query.filter(models.Customer.name.like(f"%{item.name}%"))
    if item.last_login is not None and item.last_login != 0:
        db_query = db_query.filter(models.Customer.last_login <= item.last_login + 86400)
        db_query = db_query.filter(models.Customer.last_login >= item.last_login)
    return db_query.all()


def delete_customer(db: Session, item_id: int):
    item = get_customer_once(item_id=item_id, db=db)
    if not item:
        raise Exception(f"delete failed, customer {item_id} not found")
    db.delete(item)
    db.commit()
    db.flush()
    return True


