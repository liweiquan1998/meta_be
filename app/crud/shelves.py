from typing import List

from app import models, schemas
from sqlalchemy.orm import Session
from app.crud.basic import update_to_db


def create_shelves(db: Session, item: schemas.ShelvesCreate):
    # sourcery skip: use-named-expression
    # 货架id检查
    res: models.Scene = db.query(models.Scene).filter(models.Scene.id == item.scene_id).first()
    if not res:
        raise Exception(f"场景 {item.scene_id} 不存在")
    # 创建
    db_item = models.Shelves(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_shelves(db: Session, update_item: schemas.ShelvesUpdate, item_id: int):
    return update_to_db(update_item=update_item, item_id=item_id, db=db, model_cls=models.Shelves)


def get_shelves_once(db: Session, item_id: str):
    res: models.Shelves = db.query(models.Shelves).filter(models.Shelves.shelf_id == item_id).first()
    return res


def get_shelves_all_scene(db: Session, scene_id: int):
    res: List[models.Shelves] = db.query(models.Shelves).order_by(models.Shelves.id).filter(models.Shelves.scene_id == scene_id).all()
    return res
