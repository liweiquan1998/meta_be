import json
import time
from typing import List

from app import models, schemas
from sqlalchemy.orm import Session

from app.crud import nfs
from app.crud.aigc import send_tts_request_for_blueprint
from app.crud.basic import update_to_db


def create_tts(db: Session, item: schemas.TTSCreate, text_id, sex,background_tasks):
    db_item = models.TTS(**item.dict(),
                         **{"create_time": int(time.time()), "update_time": int(time.time()), "text_id": text_id,
                            "sex": sex,"status": 0})
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    background_tasks.add_task(func=send_tts_request_for_blueprint, content=item.text_content, vh_sex=db_item.sex, mc_id=db_item.id)
    return db_item


def get_all_tts(db: Session):
    res: List[models.TTS] = db.query(models.TTS).order_by(-models.TTS.create_time).all()
    return res


def get_tts_by_text_id(db: Session, text_id: str):
    res: List[models.TTS] = db.query(models.TTS).order_by(-models.TTS.create_time).filter(models.TTS.text_id == text_id).all()
    return res


def delete_tts(db: Session, text_id: str):
    res = List[models.TTS] = db.query(models.TTS).filter(models.TTS.text_id == text_id).all()
    for item in res:
        db.delete(item)
        db.commit()
    return True


def tts_file_content(file, params, db):
    uri_dict = nfs.upload(file, 3)
    uri = uri_dict.get('uri')

    print(params)
    params = eval(params)
    item_id = params.get('mc_id')
    db_item = db.query(models.TTS).filter(models.TTS.id == item_id).first()
    if not db_item:
        raise Exception('未找到该任务')
    db_item.config_uri = uri
    db_item.status = 1
    db.commit()
    db.flush()
    db.refresh(db_item)
    return db_item
