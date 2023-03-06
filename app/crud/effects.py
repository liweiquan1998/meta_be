import time
from sqlalchemy.orm import Session
from app import models


def create_effect(db: Session, item, user):
    print(item)
    # 创建特效
    db_item = models.Effects(**item.dict(), **{'create_time': int(time.time()),
                                               'create_id': user.id,
                                               'status': 1,
                                               })
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
