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


def get_all_tts(db: Session):
    res: List[models.TTS] = db.query(models.TTS).order_by(-models.TTS.create_time).all()
    return res


def delete_tts(db: Session, text_id: int):
    res = List[models.TTS] = db.query(models.TTS).filter(models.TTS.text_id == text_id).all()
    for item in res:
        db.delete(item)
        db.commit()
    return True
