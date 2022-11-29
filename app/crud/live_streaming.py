import threading
import time
from typing import List

import requests

from app import models, schemas
from sqlalchemy.orm import Session
from app.crud.basic import update_to_db
from app.common.validation import *


def create_live_streaming(db: Session, item: schemas.LiveStreamingCreate):
    # sourcery skip: use-named-expression
    # todo 判断各参数合法性
    # 创建
    db_item = models.LiveStreaming(**item.dict(), **{'last_time': int(time.time())})
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_live_streaming(db: Session, item_id: int, update_item: schemas.LiveStreamingUpdate):
    return update_to_db(update_item=update_item, db=db, item_id=item_id, model_cls=models.LiveStreaming)


def get_live_streaming_once(db: Session, item_id: int):
    if item := db.query(models.LiveStreaming).filter(models.LiveStreaming.id == item_id).first():
        return item
    else:
        raise Exception(f"直播流id {item_id} 不存在")


def get_live_streamings(db: Session, item: schemas.LiveStreamingGet):
    db_query = db.query(models.LiveStreaming)
    if item.name:
        db_query = db_query.filter(models.LiveStreaming.name.like(f"%{item.name}%"))
    if item.create_time is not None and item.create_time != 0:
        db_query = db_query.filter(models.LiveStreaming.create_time <= item.create_time + 86400)
        db_query = db_query.filter(models.LiveStreaming.create_time >= item.create_time)
    return db_query.order_by(models.LiveStreaming.id).all()


def delete_live_streaming(db: Session, item_id: int):
    db.query(models.LiveStreaming).filter(models.LiveStreaming.id == item_id).delete()
    db.commit()
    return True
