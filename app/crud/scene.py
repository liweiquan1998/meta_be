import time
from app import models, schemas
from sqlalchemy.orm import Session
from app.crud.basic import update_to_db


def create_scene(db: Session, item: schemas.SceneCreate, user):
    # sourcery skip: use-named-expression
    # 创建
    db_item = models.Scene(**item.dict(), **{'create_time': int(time.time()),
                                             'creator_id': user.id
                                             })
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_scene(db: Session, update_item: schemas.SceneUpdate, item_id: int):
    return update_to_db(update_item=update_item, item_id=item_id, db=db, model_cls=models.Scene,
                        force=1, force_fields=('virtual_human_ids',))


def get_scene_once(db: Session, item_id: int):
    res: models.Scene = db.query(models.Scene).filter(models.Scene.id == item_id).first()
    return res


def get_scene_once_by_creator_id(db: Session, creator_id: int):
    res: models.Scene = db.query(models.Scene).filter(models.Scene.creator_id == creator_id).all()
    return res


def get_scenes(db: Session, item: schemas.SceneGet, user: models.User):
    if not item.creator_id:
        item.creator_id = user.id
    db_query = db.query(models.Scene)
    if item.creator_id is not None:
        db_query = db_query.filter(models.Scene.creator_id == item.creator_id)
    if item.name is not None and item.name != "":
        db_query = db_query.filter(models.Scene.name.like(f"%{item.name}%"))
    if item.tag is not None:
        db_query = db_query.filter(models.Scene.tag == item.tag)
    if item.base_id:
        db_query = db_query.filter(models.Scene.base_id == item.base_id)
    return db_query.order_by(-models.Scene.create_time).all()


def delete_scene(db: Session, item_id: int):
    res = get_scene_once(db=db, item_id=item_id)
    if not res:
        raise Exception(f"场景 {item_id} 不存在")
    db.delete(res)
    db.commit()
    return True
