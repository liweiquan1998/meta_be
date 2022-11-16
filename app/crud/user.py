import time
from typing import List
from app import models, schemas
from sqlalchemy.orm import Session
from app.crud.basic import update_to_db
from utils.user import *

def create_user(db: Session, item: schemas.UserCreate):
    db_item = models.User(**item.dict(), **{"create_time": int(time.time()), "update_time": int(time.time()), "last_login": int(time.time())})
    db_item.password_hash = get_password_hash(item.password_hash)
    db_item.auth_token = create_access_token(item.password_hash)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_user(db: Session, item_id: int, update_item: schemas.UserUpdate):
    return update_to_db(update_item=update_item, item_id=item_id, db=db, model_cls=models.User)


def get_user_once(db: Session, item_id: int):
    res: models.User = db.query(models.User).filter(models.User.id == item_id).first()
    return res


def get_users(db: Session):
    res: List[models.User] = db.query(models.User).all()
    return res


def delete_user(db: Session, item_id: int):
    item = get_user_once(item_id=item_id, db=db)
    if not item:
        raise Exception(f"delete failed, user {item_id} not found")
    db.delete(item)
    db.commit()
    db.flush()

