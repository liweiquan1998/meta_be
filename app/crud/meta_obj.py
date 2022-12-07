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
from app.crud.user import *
from app.crud.file import *




def meta_obj_add_username(mo, db: Session, ):
    if type(mo) == list:
        res = [r.to_dict() for r in mo]
        for m in res:
            try:
                m['creator_name'] = db.query(models.User).filter(models.User.id == m['creator_id']).first().name
            except Exception as e:
                raise Exception(f"meta_obj {m['id']} 的创建者不存在")
    else:
        res = mo.to_dict()
        res['creator_name'] = db.query(models.User).filter(models.User.id == res['creator_id']).first().name
    return res


def create_meta_obj(db: Session, item, creator_id, upload_type=None):
    # sourcery skip: use-named-expression
    # 重复名称检查
    item.name = is_valid_name(item.name, 10)
    res: models.MetaObj = db.query(models.MetaObj).filter(models.MetaObj.name == item.name).first()
    if res:
        raise Exception(f"物品 {item.name} 已存在")
    # 场景素材
    if item.type == 1:
        create_meta_obj_tag(db, item.tag)

    # 创建
    db_item = models.MetaObj(**item.dict(), **{'create_time': int(time.time()),
                                               'creator_id': creator_id,
                                               'kind': 0 if upload_type is None else 1,
                                               'status': 0 if item.type == 0 else None})

    if upload_type == 'image':
        # db_item.thumbnail = item.aigc[0]
        minio_path = item.aigc[0]
        file_byte = get_minio_file_byte(minio_path)
        nfs_path = f"SceneAssets/{minio_path}"
        with open(f"/mnt/nfs/{nfs_path}", "wb") as f:
            f.write(file_byte)
        db_item.thumbnail = nfs_path
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    # 由图片流创建模型
    if item.type == 0:
        threading.Thread(target=send_nerf_request, args=(item.aigc, db_item.id, upload_type)).start()
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
    item = db.query(models.MetaObj).filter(models.MetaObj.id == item_id).first()
    if not item:
        raise Exception(f"meta_obj {item_id} 不存在")
    db.delete(item)
    db.commit()
    db.flush()
    return True
