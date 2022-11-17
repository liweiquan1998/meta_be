import time
from typing import List
from app import models, schemas
from sqlalchemy.orm import Session
from app.crud.basic import update_to_db
from app.common.validation import *

def create_admin(db: Session, item: schemas.AdminCreate):
    db_item = models.Admin(**item.dict(), **{"create_time": int(time.time()),
                                             "update_time": int(time.time()),
                                             "last_login": int(time.time())})
    db_item.password_hash = get_password_hash(item.password_hash)
    db_item.auth_token = create_access_token(item.password_hash)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_admin(db: Session, item_id: int, update_item: schemas.AdminUpdate):
    return update_to_db(update_item=update_item, item_id=item_id, db=db, model_cls=models.Admin)

def get_admin_once(db: Session, item_id: int):
    res: models.Admin = db.query(models.Admin).filter(models.Admin.id == item_id).first()
    return res

def get_admins(db: Session):
    res: List[models.Admin] = db.query(models.Admin).all()
    return res


def delete_admin(db: Session, item_id: int):
    item = get_admin_once(item_id=item_id, db=db)
    if not item:
        raise Exception(f"delete failed, admin {item_id} not found")
    db.delete(item)
    db.commit()
    db.flush()