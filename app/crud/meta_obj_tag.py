import time
from typing import List
from app import models, schemas
from sqlalchemy.orm import Session
from app.crud.basic import update_to_db
from app.common.validation import *
from utils.valid_name import is_valid_name


def create_meta_obj_tag(db: Session, tag: str):
    # sourcery skip: use-named-expression
    tag = is_valid_name(tag, 10)
    res: models.MetaObjTag = db.query(models.MetaObjTag).filter(models.MetaObjTag.name == tag).first()
    if res:
        return res
    db_item = models.MetaObjTag(**{"name": tag})
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_meta_obj_tag(db: Session):
    return db.query(models.MetaObjTag).all()


def delete_meta_obj_tag(db: Session, item_id: int):
    item = db.query(models.MetaObjTag).filter(models.MetaObjTag.id == item_id).first()
    if not item:
        raise Exception(f"meta_obj_tag {item_id} 不存在")
    db.delete(item)
    db.commit()
    db.flush()
    return True
