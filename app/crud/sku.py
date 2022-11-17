from typing import List
from app import models, schemas
from sqlalchemy.orm import Session
from app.crud.basic import update_to_db


def create_sku(db: Session, item: schemas.SkuCreate):
    db_item = models.Sku(**item.dict())
    if db_item.stock == 0:
        db_item.status = 0
    else:
        db_item.status = 1
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_sku(db: Session, item_id: int, update_item: schemas.SkuUpdate):
    if update_item.stock == 0:
        status = 0
    else:
        status = 1
    return update_to_db(update_item=update_item, item_id=item_id, db=db, model_cls=models.Sku,extra=("status",status))

def get_sku_once(db: Session, item_id: int):
    res: models.Sku = db.query(models.Sku).filter(models.Sku.id == item_id).first()
    return res


def get_skus(db: Session):
    res: List[models.Sku] = db.query(models.Sku).all()
    return res


def delete_sku(db: Session, item_id: int):
    item = get_sku_once(item_id=item_id, db=db)
    if not item:
        raise Exception(f"delete failed, sku {item_id} not found")
    db.delete(item)
    db.commit()
    db.flush()

