import time
from typing import List
from app import models, schemas
from sqlalchemy.orm import Session
from app.crud.basic import update_to_db
from app.common.validation import *
from configs.settings import config

ACCESS_TOKEN_EXPIRE_MINUTES = config.get('USER', 'expire_minutes')
LOGIN_EXPIRED = config.get('USER', 'login_expired')


def create_user(db: Session, item: schemas.UserCreate):
    # sourcery skip: use-named-expression
    # 重复用户名检查
    res: models.User = db.query(models.User).filter(models.User.name == item.name).first()
    if res:
        raise Exception(f"用户 {item.name} 已存在")
    # 重复店铺名检查
    res: models.User = db.query(models.User).filter(models.User.storename == item.storename).first()
    if res:
        raise Exception(f"店铺名 {item.storename} 已存在")
    # 创建
    password = item.password
    del item.password
    db_item = models.User(**item.dict(), **{'password_hash': get_password_hash(password),
                                            "create_time": int(time.time()),
                                            "update_time": int(time.time()),
                                            "last_login": int(time.time()),
                                            "status": 0})
    db_item.auth_token = create_access_token(db_item.id, 'user')
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def login_user_swagger(db: Session, item: schemas.UserLogin):
    res: models.User = db.query(models.User).filter(models.User.name == item.name).first()
    # 用户不存在
    if not res:
        raise Exception(404, f"用户 {item.name} 不存在")
    # 密码错误
    if not verify_password(item.password, res.password_hash):
        raise Exception(401, "用户密码错误")
    res.auth_token = create_access_token(res.id, 'user')
    db.commit()
    db.flush()
    return TokenSchemas(**{"access_token": res.auth_token, "token_type": "bearer"})


def login_user(db: Session, item: schemas.UserLogin):
    res: models.User = db.query(models.User).filter(models.User.name == item.name).first()
    allow_ue = 1  # 允许该token连接ue的ws
    # 用户不存在
    if not res:
        raise Exception(404, f"用户 {item.name} 不存在")
    # 密码错误
    if not verify_password(item.password, res.password_hash):
        raise Exception(401, "用户密码错误")
    if time.time() - res.last_ping > int(LOGIN_EXPIRED):
        res.occupied = 0
    # 已被占用
    if res.occupied == 1:
        raise Exception(401, '该账户已经被其他客户端占用')
        # allow_ue = 0
    # 更新登录时间
    res.auth_token = create_access_token(res.id, 'user')
    res.last_login = int(time.time())
    db.commit()
    db.flush()
    return {"access_token": res.auth_token, "token_type": "bearer", "user_id": res.id,
            "user_name": res.name, "allow_ue": allow_ue}


def update_user(db: Session, item_id: int, update_item: schemas.UserUpdate):
    return update_to_db(update_item=update_item, item_id=item_id, db=db, model_cls=models.User)


def get_user_once(db: Session, item_id: int):
    res: models.User = db.query(models.User).filter(models.User.id == item_id).first()
    return res


def get_user_once_by_name(db: Session, name: str):
    res: models.User = db.query(models.User).filter(models.User.name == name).first()
    return res


def get_users(db: Session, item: schemas.UserGet):
    db_query = db.query(models.User)
    if item.storename:
        db_query = db_query.filter(models.User.storename.like(f"%{item.storename}%"))
    if item.create_time is not None and item.create_time != 0:
        db_query = db_query.filter(models.User.create_time <= item.create_time + 86400)
        db_query = db_query.filter(models.User.create_time >= item.create_time)
    if item.last_login is not None and item.last_login != 0:
        db_query = db_query.filter(models.User.last_login <= item.last_login + 86400)
        db_query = db_query.filter(models.User.last_login >= item.last_login)
    if item.status:
        db_query = db_query.filter(models.User.status == item.status)
    return db_query.all()


def delete_user(db: Session, item_id: int):
    item = get_user_once(item_id=item_id, db=db)
    if not item:
        raise Exception(404, f"删除失败, 用户 {item_id} 不存在")
    db.delete(item)
    db.commit()
    db.flush()
    return True

