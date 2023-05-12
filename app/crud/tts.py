import json
import time
from typing import List

from app import models, schemas
from sqlalchemy.orm import Session
from app.crud.basic import update_to_db


def create_tts(db: Session, item: schemas.TTSCreate):
    db_item = models.TTS(**item.dict(), **{"create_time": int(time.time()),
                                           "update_time": int(time.time())})
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_tts(db: Session, item_id: int, update_item: schemas.TTSUpdate):
    return update_to_db(update_item=update_item, item_id=item_id, db=db, model_cls=models.TTS)



def get_tts_once_pop(db: Session, item_id: int):
    res: models.TTS = db.query(models.TTS).filter(models.TTS.pop_id == item_id).first()
    return res


def get_all_tts_blueprint(db: Session,blueprint_id: int):
    res: List[models.TTS] = db.query(models.TTS).filter(models.TTS.blueprint_id == blueprint_id).order_by(-models.TTS.create_time).all()
    return res


def get_all_tts(db: Session):
    res: List[models.TTS] = db.query(models.TTS).order_by(-models.TTS.create_time).all()
    return res


def delete_tts(db: Session, item_id: int):
    db.query(models.TTS).filter(models.TTS.id == item_id).delete()
    db.commit()
    return True
