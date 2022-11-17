import time
from typing import List
from app import models, schemas
from sqlalchemy.orm import Session
from app.crud.basic import update_to_db
from app.common.validation import *


def create_admin(db: Session, item: schemas.AdminCreate):
    # sourcery skip: use-named-expression
    # 重复用户名检查
    res: models.Admin = db.query(models.Admin).filter(models.Admin.username == item.username).first()
    if res:
        raise Exception(f"用户 {item.username} 已存在")
    # 创建
    password = item.password
    del item.password
    db_item = models.Admin(**item.dict(), **{'password_hash': get_password_hash(password),
                                             "create_time": int(time.time()),
                                             "update_time": int(time.time()),
                                             "last_login": int(time.time())})
    db_item.auth_token = create_access_token(db_item.username, 'admin')
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def login_admin_api(db: Session, item: schemas.AdminLogin):
    res: models.Admin = db.query(models.Admin).filter(models.Admin.username == item.username).first()
    # 用户不存在
    if not res:
        raise Exception(404, f"用户 {item.username} 不存在")
    # 密码错误
    if not verify_password(item.password, res.password_hash):
        raise Exception(401, "密码错误")
    # 更新登录时间
    res.auth_token = create_access_token(res.username, 'admin')
    res.last_login = int(time.time())
    db.commit()
    db.flush()
    return TokenSchemas(**{"access_token": res.auth_token, "token_type": "bearer"})


def login_admin(db: Session, item: schemas.AdminLogin):
    res: models.Admin = db.query(models.Admin).filter(models.Admin.username == item.username).first()
    # 用户不存在
    if not res:
        raise Exception(404, f"用户 {item.username} 不存在")
    # 密码错误
    if not verify_password(item.password, res.password_hash):
        raise Exception(401, "密码错误")
    # 更新登录时间
    res.auth_token = create_access_token(res.username, 'admin')
    res.last_login = int(time.time())
    db.commit()
    db.flush()
    # return {"access_token": res.auth_token, "token_type": "bearer"}
    return res


def update_admin(db: Session, item_id: int, update_item: schemas.AdminUpdate):
    return update_to_db(update_item=update_item, item_id=item_id, db=db, model_cls=models.Admin)


def get_admin_once(db: Session, item_id: int):
    res: models.Admin = db.query(models.Admin).filter(models.Admin.id == item_id).first()
    return res


def get_admin_once_by_username(db: Session, username: str):
    res: models.Admin = db.query(models.Admin).filter(models.Admin.username == username).first()
    return res


def get_admins(db: Session):
    res: List[models.Admin] = db.query(models.Admin).all()
    return res


def delete_admin(db: Session, item_id: int):
    item = get_admin_once(item_id=item_id, db=db)
    if not item:
        raise Exception(f"delete failed, admin {item_id} not found")
    db.delete(item)
    db.commit()
    db.flush()
