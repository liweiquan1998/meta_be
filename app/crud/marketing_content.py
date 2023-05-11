import threading
import time
from app import models, schemas
from sqlalchemy.orm import Session
from app.core.storage.file import MinioStorage
from app.crud.basic import update_to_db
from app.crud.aigc import send_tts_request, send_compose_request

minio = MinioStorage()


def mc_add_username(mc, db: Session):
    if type(mc) == list:
        res = [r.to_dict() for r in mc]
        for m in res:
            try:
                m['creator_name'] = db.query(models.User).filter(models.User.id == m['creator_id']).first().name
            except Exception as e:
                raise Exception(f"营销内容id {m['id']} 的创建者id {m['creator_id']} 不存在") from e
    else:
        res = mc.to_dict()
        res['creator_name'] = db.query(models.User).filter(models.User.id == res['creator_id']).first().name
    return res


def create_marketing_content(db: Session, item: schemas.MarketingContentCreate, creator_id: int, background_tasks):
    # sourcery skip: use-named-expression
    # meta_obj 存在检查
    if db.query(models.MetaObj).filter(models.MetaObj.id == item.metaobj_id).first() is None:
        raise Exception(f"meta_obj {item.metaobj_id} 不存在")
    if not db.query(models.MarketingContent).filter(models.MarketingContent.name == item.name).first() is None:
        raise Exception(f"内容标题 {item.name} 重复")
    # 创建者 存在检查
    if db.query(models.User).filter(models.User.id == creator_id).first() is None:
        raise Exception(f"创建者 {creator_id} 不存在")
    # 删除virtual_human_sex
    vh_sex = 0 if item.virtual_human_sex < 1 else 1
    item.virtual_human_sex = vh_sex
    # 创建 添加create_id
    db_item = models.MarketingContent(**item.dict(), **{'create_time': int(time.time()),
                                                        'creator_id': creator_id,
                                                        'status': 0})
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    background_tasks.add_task(func=send_tts_request, content=item.content, vh_sex=vh_sex, mc_id=db_item.id)
    return db_item


def compose_video(db: Session, item: schemas.ComposeVideo):
    res = db.query(models.MarketingContent).filter(models.MarketingContent.id == item.marketing_content_id).first()
    res.status = 3
    db.commit()
    print(item.video_uri)
    print("====")
    print(res.audio_uri)
    # threading.Thread(target=send_compose_request,
    #                  args=(item.video_uri, res.audio_uri, item.marketing_content_id)).start()
    return False


def update_marketing_content(db: Session, item_id: int, update_item: schemas.MarketingContentUpdate):
    return update_to_db(update_item=update_item, db=db, item_id=item_id, model_cls=models.MarketingContent)


def update_marketing_content_by_workspace(db: Session, workspace: str, update_item: schemas.MarketingContentUpdate):
    db_query = db.query(models.MarketingContent)
    db_query = db_query.filter(models.MarketingContent.work_space == workspace)
    db_query.update(update_item.dict(exclude_unset=True))
    db.commit()
    return True


def get_marketing_content_once(db: Session, item_id: int):
    if item := db.query(models.MarketingContent).filter(models.MarketingContent.id == item_id).first():
        return mc_add_username(item, db)
    else:
        raise Exception(f"营销内容id {item_id} 不存在")


def get_marketing_contents(db: Session, item: schemas.MarketingContentGet):
    db_query = db.query(models.MarketingContent)
    if item.creator_id:
        db_query = db_query.filter(models.MarketingContent.creator_id == item.creator_id)
    if item.name:
        db_query = db_query.filter(models.MarketingContent.name.like(f"%{item.name}%"))
    if item.status is not None:
        db_query = db_query.filter(models.MarketingContent.status == item.status)
    if item.create_time is not None:
        db_query = db_query.filter(models.MarketingContent.create_time <= item.create_time + 86400)
        db_query = db_query.filter(models.MarketingContent.create_time >= item.create_time)
    res = db_query.order_by(-models.MarketingContent.create_time).all()
    return mc_add_username(res, db)


def delete_marketing_content(db: Session, item_id: int):
    item = db.query(models.MarketingContent).filter(models.MarketingContent.id == item_id).first()
    if not item:
        raise Exception(f"营销内容id {item_id} 不存在")
    db.delete(item)
    db.commit()
    return True


def market_file_content(file, params, db):
    uri_dict = minio.upload(file)
    uri = uri_dict.get('uri')
    file_type = uri.split('.')[-1]
    print(params)
    params = eval(params)
    item_id = params.get('mc_id')
    db_item = db.query(models.MarketingContent).filter(models.MarketingContent.id == item_id).first()
    if not db_item:
        raise Exception('未找到该任务')
    if file_type == 'wav':
        db_item.status = 2
        db_item.audio_uri = uri
    else:
        db_item.status = 4
        db_item.video_uri = uri
    db.commit()
    db.flush()
    db.refresh(db_item)
    return db_item

