import time
from typing import List
from app import models, schemas
from sqlalchemy.orm import Session
from app.crud.basic import update_to_db


def get_scene_base(db: Session, item: schemas.SceneBaseGet):
    db_query = db.query(models.SceneBase)
    if item.name:
        db_query = db_query.filter(models.SceneBase.name.like(f"%{item.name}%"))
    return db_query.all()


def get_scene_base_once(db: Session, item_id: int):
    return db.query(models.SceneBase).filter(models.SceneBase.id == item_id).first()
