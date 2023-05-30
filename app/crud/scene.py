import time
from app import models, schemas
from sqlalchemy.orm import Session
from app.crud.basic import update_to_db

# 创建场景
def create_scene(db: Session, item: schemas.SceneCreate, user):
    check_item: models.Scene = db.query(models.Scene).filter(models.Scene.name == item.name).first()
    if check_item:
        raise Exception(f"场景名称 {item.name} 已存在")
    # 创建
    db_item = models.Scene(
        **item.dict(),
        **{
            'create_id': user.id,
            'create_time': int(time.time()),
            'update_id': user.id,
            'update_time': int(time.time()),
        })
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# 修改场景
def update_scene(db: Session, update_item: schemas.SceneUpdate, item_id: int, user: models.User):
    db_item: models.Scene = db.query(models.Scene).filter(models.Scene.id == item_id).first()
    if not db_item:
        raise Exception(f"场景 {item_id} 不存在")
    for k, v in update_item.dict(exclude_unset=True).items():
        setattr(db_item, k, v)
    db_item.update_id = user.id
    db_item.update_time = int(time.time())
    db.commit()
    db.flush()
    db.refresh(db_item)
    return db_item

# 获取场景详情
def get_scene_once(db: Session, item_id: int):
    db_item: models.Scene = db.query(models.Scene).filter(models.Scene.id == item_id).first()
    if not db_item:
        raise Exception(f"场景 {item_id} 不存在")
    return db_item

# 获取场景列表
def get_scenes(db: Session, item: schemas.SceneGet, user: models.User):
    db_query = db.query(models.Scene).filter(models.Scene.create_id == user.id)
    if item.name is not None and item.name != "":
        db_query = db_query.filter(models.Scene.name.like(f"%{item.name}%"))
    if item.tag is not None:
        db_query = db_query.filter(models.Scene.tag == item.tag)
    if item.stage is not None:
        db_query = db_query.filter(models.Scene.stage == item.stage)
    return db_query.order_by(-models.Scene.create_time).all()

# 删除场景
def delete_scene(db: Session, item_id: int):
    db_item: models.Scene = get_scene_once(db=db, item_id=item_id)
    db.delete(db_item)
    db.commit()
    return db_item
