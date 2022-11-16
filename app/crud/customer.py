import time
from typing import List
from app import models, schemas
from sqlalchemy.orm import Session
from app.crud.basic import update_to_db
from utils.user import *

def create_customer(db: Session, item: schemas.CustomerCreate):
    db_item = models.Customer(**item.dict(), **{"create_time": int(time.time()), "update_time": int(time.time()), "last_login": int(time.time())})
    db_item.password_hash = get_password_hash(item.password_hash)
    db_item.auth_token = create_access_token(item.password_hash)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_customer(db: Session, item_id: int, update_item: schemas.CustomerUpdate):
    return update_to_db(update_item=update_item, item_id=item_id, db=db, model_cls=models.Customer)


def get_customer_once(db: Session, item_id: int):
    res: models.Customer = db.query(models.Customer).filter(models.Customer.id == item_id).first()
    return res


def get_customers(db: Session):
    res: List[models.Customer] = db.query(models.Customer).all()
    return res


def delete_customer(db: Session, item_id: int):
    item = get_customer_once(item_id=item_id, db=db)
    if not item:
        raise Exception(f"delete failed, customer {item_id} not found")
    db.delete(item)
    db.commit()
    db.flush()

