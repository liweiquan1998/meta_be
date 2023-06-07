import json
import time
from app import models, schemas
from sqlalchemy.orm import Session
from app.crud.basic import update_to_db


def create_store(db: Session, item: schemas.StoreCreate, user: models.User):
    # sourcery skip: use-named-expression
    # 重复店铺名检查

    if db.query(models.Store).filter(models.Store.name == item.name).first():
        raise Exception(f"店铺名 {item.name} 已存在")
    if db.query(models.Scene).filter(models.Scene.id == item.scene_id).first() is None:
        raise Exception(f"场景id {item.scene_id} 不存在")
    if db.query(models.User).filter(models.User.id == item.creator_id).first() is None:
        raise Exception(f"创建者id {item.creator_id} 不存在")

    virtual_human_id = item.dict().get("virtual_human_id")
    if not db.query(models.VirtualHuman).filter(models.VirtualHuman.id == virtual_human_id).first():
        return Exception(f'虚拟人 {virtual_human_id} 不存在')
    dic = item.dict()
    dic.pop("virtual_human_id")
    db_item = models.Store(**dic, **{"create_time": int(time.time()),
                                     "creator_name": db.query(models.User).filter(
                                         models.User.id == item.creator_id).first().name})
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    # 店铺创建之后：
    # 被使用类型：虚拟人；使用场景：店铺；店铺的id 被使用者：虚拟人id
    relation_dict = {
        "relation_type": "virtual_human",
        "usage_scenario": "store",
        "subject_id": db_item.id,
        "entity_id": virtual_human_id
    }
    db_relation = models.Relation(**relation_dict)
    db.add(db_relation)
    db.commit()
    db.refresh(db_relation)
    # 这里如果不print会返回一个空数据
    return db_item.to_dict()


def update_store(db: Session, item_id: int, update_item: schemas.StoreUpdate, user: models.User):
    if update_item.sku_ids is None:
        update_item.sku_ids = ""
    virtual_human_id = update_item.virtual_human_id
    update_item.virtual_human_id = None
    flag = db.query(models.VirtualHuman).filter(models.VirtualHuman.id == virtual_human_id).filter(
        models.VirtualHuman.creator_id == user.id).first()
    if not flag:
        raise Exception(f"虚拟人 {virtual_human_id} 不存在")
    res = update_to_db(update_item=update_item, item_id=item_id, db=db, model_cls=models.Store, force=1,
                       force_fields=('sku_ids',))
    db.query(models.Relation).filter(models.Relation.subject_id == item_id).filter(
        models.Relation.relation_type == "virtual_human").filter(models.Relation.usage_scenario=="store").delete()

    data_dic = {
        "relation_type": "virtual_human",
        "usage_scenario": "store",
        "subject_id": item_id,
        "entity_id": virtual_human_id
    }
    obj = models.Relation(**data_dic)
    db.add(obj)
    db.commit()
    return res.to_dict()


def get_store_once(db: Session, item_id: int):
    res: models.Store = db.query(models.Store).filter(models.Store.id == item_id).first()
    return res


def get_stores(db: Session, item: schemas.StoreGet, user: models.User):
    if not item.creator_id:
        item.creator_id = user.id
    db_query = db.query(models.Store)
    if item.creator_id:
        db_query = db_query.filter(models.Store.creator_id == item.creator_id)
    if item.name:
        db_query = db_query.filter(models.Store.name.like(f"%{item.name}%"))
    return db_query.order_by(-models.Store.create_time).all()


def delete_store(db: Session, item_id: int):
    if not db.query(models.Store).filter(models.Store.id == item_id):
        raise Exception(f'商铺 {item_id} 不存在 ')
    db.query(models.Store).filter(models.Store.id == item_id).delete()
    db.query(models.Relation).filter(models.Relation.subject_id == item_id).filter(
        models.Relation.relation_type == "virtual_human").filter(models.Relation.usage_scenario == "store").delete()
    db.commit()
    return True
