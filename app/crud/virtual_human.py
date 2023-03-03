import time
from typing import List
from app import models, schemas
from sqlalchemy.orm import Session
from app.crud.basic import update_to_db
from app.common.validation import *


def create_virtual_human(db: Session, item: schemas.VirtualHumanCreate, user: models.User):
    # sourcery skip: use-named-expression
    # 重复虚拟人检查
    # item.creator_id = user.id
    res: models.VirtualHuman = db.query(models.VirtualHuman).filter(models.VirtualHuman.name == item.name).first()
    # if res:
    #     raise Exception(f"虚拟人 {item.name} 已存在")
    # 性别及状态检查
    if item.sex not in [0, 1, 2]:
        raise Exception(f'虚拟人性别出错 实为{item.sex} 应为 0:未知 1:男 2:女')
    if item.status not in [0, 1]:
        raise Exception(f'虚拟人状态出错 实为{item.status} 应为 0:禁用 1:启用')
    # 创建
    db_item = models.VirtualHuman(**item.dict(), **{'create_time': int(time.time()),
                                                    'creator_id': user.id
                                                    })
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_virtual_human(db: Session, item_id: int, update_item: schemas.VirtualHumanUpdate):
    return update_to_db(update_item=update_item, db=db, item_id=item_id, model_cls=models.VirtualHuman)


def get_virtual_human_once(db: Session, item_id: int):
    if item := db.query(models.VirtualHuman).filter(models.VirtualHuman.id == item_id).first():
        return item
    else:
        raise Exception(f"虚拟人id {item_id} 不存在")


def get_virtual_human_once_by_creator_id(db: Session, creator_id: int):
    if item := db.query(models.VirtualHuman).filter(models.VirtualHuman.creator_id == creator_id).all():
        return item
    else:
        raise Exception(f"虚拟人id {creator_id} 不存在")


def get_virtual_humans(db: Session, item: schemas.VirtualHumanGet, user: models.User):
    db_query = db.query(models.VirtualHuman)
    if not item.creator_id:
        item.creator_id = user.id
    if item.creator_id:
        db_query = db_query.filter(models.VirtualHuman.creator_id == item.creator_id)
    if item.name:
        db_query = db_query.filter(models.VirtualHuman.name.like(f"%{item.name}%"))
    if item.sex is not None:
        db_query = db_query.filter(models.VirtualHuman.sex == item.sex)
    return db_query.order_by(models.VirtualHuman.id).all()


def delete_virtual_human(db: Session, item_id: int, user: models.User):
    item: models.VirtualHuman = db.query(models.VirtualHuman).filter(models.VirtualHuman.id == item_id).first()
    if not item:
        raise Exception(f"虚拟人 {item_id} 不存在")
    select_vh_ids_sql = '''SELECT json_array_elements(virtual_human_ids) as vh_id,name
                                 from scene
                                 where creator_id='{}'
                                 '''.format(user.id)
    vh_ids_rows = db.execute(select_vh_ids_sql).fetchall()
    if vh_ids_rows:
        scene_names = [row[1] for row in vh_ids_rows if row[0] == item_id]
        if scene_names:
            raise Exception(400, f'该虚拟人已经被{scene_names}使用，不可以在本页面下架')
    db.delete(item)
    db.commit()
    db.flush()
    return True
