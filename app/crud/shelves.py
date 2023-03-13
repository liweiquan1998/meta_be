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


def get_shelves_once(db: Session, item_id: int):
    res: models.Shelves = db.query(models.Shelves).filter(models.Shelves.id == item_id).first()
    return res


def get_shelves_once_by_creator_id(db: Session, creator_id: int):
    res: models.Shelves = db.query(models.Shelves).filter(models.Shelves.creator_id == creator_id).al()
    return res


def get_shelves(db: Session, item: schemas.ShelvesGet):
    db_query = db.query(models.Shelves)
    if item.scene_id:
        db_query = db_query.filter(models.Shelves.scene_id == item.scene_id)
    return db_query.order_by(models.Shelves.id).all()
