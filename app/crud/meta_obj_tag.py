from app import models
from sqlalchemy.orm import Session
from utils.valid_name import is_valid_name


def create_meta_obj_tag(db: Session, tag: str, creator_id: int):
    # sourcery skip: use-named-expression
    tag = is_valid_name(tag, 10)
    res: models.MetaObjTag = db.query(models.MetaObjTag).filter(models.MetaObjTag.name == tag).filter(models.MetaObjTag.creator_id == creator_id).first()
    if res:
        return res
    db_item = models.MetaObjTag(**{"name": tag, "creator_id": creator_id})
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_meta_obj_tag(db: Session,creator_id: int):
    res: models.MetaObjTag = db.query(models.MetaObjTag).order_by(models.MetaObjTag.id).filter(models.MetaObjTag.creator_id == creator_id).all()
    if res:
        return res
    else:
        raise Exception("该用户没有元对象标签")


def delete_meta_obj_tag(db: Session, item_id: int):
    item = db.query(models.MetaObjTag).filter(models.MetaObjTag.id == item_id).first()
    if not item:
        raise Exception(f"meta_obj_tag {item_id} 不存在")
    db.delete(item)
    db.commit()
    db.flush()
    return True
