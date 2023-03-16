import time
from sqlalchemy.orm import Session
from app import models


def create_marketing_component(db: Session, item):
    db_item = models.MarketingComponent(**item.dict(), **{'create_time': int(time.time()),
                                                          })
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_marketing_component(db: Session, item):
    db_query = db.query(models.MarketingComponent).filter(models.MarketingComponent.type == item.type)
    return db_query.order_by(models.MarketingComponent.id).all()


def update_marketing_component(db: Session, item, item_id):
    db_item = db.query(models.MarketingComponent).filter(models.MarketingComponent.id == item_id).first()
    db_item.content = item.content
    db_item.update_time = int(time.time())
    db.commit()
    db.flush()
    db.refresh(db_item)
    return db_item


def delete_marketing_component(db: Session, item_id):
    db.query(models.MarketingComponent).filter(models.MarketingComponent.id == item_id).delete()
    db.commit()
    return True
