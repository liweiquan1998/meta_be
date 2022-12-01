import threading
import time
from typing import List
from app import models, schemas
from sqlalchemy.orm import Session
from app.crud.basic import update_to_db
from app.common.validation import *
from app.crud.meta_obj_tag import create_meta_obj_tag
from utils.valid_name import is_valid_name
from app.crud.aigc import *


def userid2name(user_id: int, db: Session):
    if user := db.query(models.User).filter(models.User.id == user_id).first():
        return user.name
    else:
        raise Exception(f"用户 {user_id} 不存在")


def meta_obj_add_username(mo, db: Session, ):
    if type(mo) == list:
        res = [r.to_dict() for r in mo]
        for m in res:
            m['creator_name'] = userid2name(m['creator_id'], db)
    else:
        res = mo.to_dict()
        res['creator_name'] = userid2name(res['creator_id'], db)
    return res


def create_meta_obj(db: Session, item):
    # sourcery skip: use-named-expression
    # 重复名称检查
    item.name = is_valid_name(item.name, 10)
    res: models.MetaObj = db.query(models.MetaObj).filter(models.MetaObj.name == item.name).first()
    if res:
        raise Exception(f"物品 {item.name} 已存在")
    if item.type == 0:
        create_meta_obj_tag(db, item.tag)
    # 由图片流创建模型
    if item.type in [1, 2]:
        item.status = 0
        threading.Thread(target=send_nerf_request, args=(item.aigc, item.id, 'image' if item.status == 1 else 'video')).start()

    # 创建
    db_item = models.MetaObj(**item.dict(), **{'create_time': int(time.time())})
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_meta_obj(db: Session, item_id: int, update_item: schemas.MetaObjUpdate):
    return update_to_db(update_item=update_item, item_id=item_id, db=db, model_cls=models.MetaObj)


def get_meta_obj_once(db: Session, item_id: int):
    res: models.MetaObj = db.query(models.MetaObj).filter(models.MetaObj.id == item_id).first()
    return meta_obj_add_username(res, db)


def get_meta_obj_by_creator_id(db: Session, creator_id: int):
    meta_objs = db.query(models.MetaObj).filter(models.MetaObj.creator_id == creator_id).all()
    return meta_obj_add_username(meta_objs, db)


def get_meta_objs(db: Session, item: schemas.MetaObjGet):
    # sourcery skip: inline-immediately-returned-variable
    db_query = db.query(models.MetaObj)
    if item.name and item.name != "":
        db_query = db_query.filter(models.MetaObj.name.like(f"%{item.name}%"))
    if item.kind is not None and item.kind != -1:
        db_query = db_query.filter(models.MetaObj.kind == item.kind)
    if item.type is not None and item.type != -1:
        db_query = db_query.filter(models.MetaObj.type == item.type)
    if item.status is not None and item.status != -1:
        db_query = db_query.filter(models.MetaObj.status == item.status)
    if item.create_time is not None and item.create_time != -1:
        db_query = db_query.filter(models.MetaObj.create_time <= item.create_time + 86400)
        db_query = db_query.filter(models.MetaObj.create_time >= item.create_time)
    if item.tag is not None and item.tag != "":
        db_query = db_query.filter(models.MetaObj.tag == item.tag)
    if item.creator_id is not None and item.creator_id != -1:
        db_query = db_query.filter(models.MetaObj.creator_id == item.creator_id)

    meta_objs = db_query.all()
    return meta_obj_add_username(meta_objs, db)


def delete_meta_obj(db: Session, item_id: int):
    item = get_meta_obj_once(db, item_id)
    if not item:
        raise Exception(f"meta_obj {item_id} 不存在")
    db.delete(item)
    db.commit()
    db.flush()
    return True
