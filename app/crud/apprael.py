from sqlalchemy.orm import Session
from app import schemas, models
from app.crud.basic import update_to_db



def create_apparel(db: Session, item: schemas.ApparelCreate):
    db_item = models.Apparel(**item.dict())
    check_item = db.query(models.Apparel).filter(models.Apparel.work_space == item.work_space).first()
    if check_item:
        raise Exception('work_space has existed')
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_apparel(db: Session, item_id: int, update_item: schemas.ApparelUpdate):
    return update_to_db(update_item=update_item, db=db, item_id=item_id, model_cls=models.Apparel)


def get_apparel_once(db: Session, item_id: int):
    if item := db.query(models.Apparel).filter(models.Apparel.id == item_id).first():
        return item
    else:
        raise Exception(f"直播账号id {item_id} 不存在")


def get_apparels(db: Session, item: schemas.ApparelParams):
    db_query = db.query(models.Apparel)
    if item.apparel_name:
        db_query = db_query.filter(models.Apparel.apparel_name.like(f"%{item.apparel_name}%"))
    if item.apparel_type:
        db_query = db_query.filter(models.Apparel.apparel_type.like(f"%{item.apparel_type}%"))
    return db_query.order_by(models.Apparel.id).all()


def delete_apparel(db: Session, item_id: int):
    db_item = db.query(models.Apparel).filter(models.Apparel.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return True
    else:
        raise Exception('不存在的apparel  id')
