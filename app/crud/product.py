from typing import List
from app import models, schemas
from sqlalchemy.orm import Session
from app.crud.basic import update_to_db


def create_product(db: Session, item: schemas.ProductCreate):
    db_item = models.Product(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_product(db: Session, item_id: int, update_item: schemas.ProductUpdate):
    return update_to_db(update_item=update_item, item_id=item_id, db=db, model_cls=models.Product)

def get_product_once(db: Session, item_id: int):
    res: models.Product = db.query(models.Product).filter(models.Product.id == item_id).first()
    return res


def get_products(db: Session):
    res: List[models.Product] = db.query(models.Product).all()
    return res


def delete_product(db: Session, item_id: int):
    item = get_product_once(item_id=item_id, db=db)
    if not item:
        raise Exception(f"delete failed, customer {item_id} not found")
    db.delete(item)
    db.commit()
    db.flush()

