import time
import asyncio
from typing import List

import websockets.exceptions

from app import models, schemas
from sqlalchemy.orm import Session
from app.crud.basic import update_to_db
from app.common.validation import *
import os

ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('user_expire_minutes', '4320')
LOGIN_EXPIRED = int(os.getenv('user_login_expired', '30'))
PING_INTERVAL = int(os.getenv('user_ping_interval', '10'))
ping_uid_list = list()


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
    if time.time() - res.last_ping > LOGIN_EXPIRED:
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


async def check_alive(websocket, db, user):
    # 保证ws连接---user_id 的一对一关系 (否则可能出现a客户端断网，b登录，a刷新后共2个客户端共用1个账户的问题)
    # if user.id not in ping_uid_list:
    #     ping_uid_list.append(user.id)
    # else:
    #     raise websockets.exceptions.SecurityError

    # ws连接的心跳检测以及对user表的更新
    await websocket.accept()
    print(f'客户端连接：user={user.name}')
    retry = 0
    try:
        while True:
            try:
                await websocket.send_text('1')
                data = await asyncio.wait_for(websocket.receive_text(), 0.1)
                if data == '0':
                    print(f'客户端正常退出,user={user.name}')
                    user.occupied = 0
                    db.commit()
                    db.flush()
                    break
                user.last_ping = int(time.time())
                user.occupied = 1
                db.commit()
                db.flush()
                retry = 0
                print(f'ping_user={user.name}:ok')
                await asyncio.sleep(PING_INTERVAL)
            except Exception as e:
                retry += 1
                print(f'websocket 心跳异常: retry={retry}, user={user.name},e:{str(e)}')
                if retry >= LOGIN_EXPIRED//PING_INTERVAL:
                    print(f'{retry}次心跳失败,websocket关闭,user={user.name},exception:{str(e)}')
                    user.occupied = 0
                    db.commit()
                    db.flush()
                    await websocket.close()
                    break
                await asyncio.sleep(PING_INTERVAL)
    finally:

        # 保证连接断开后一定清除掉user_id，否则一直占用会导致客户端无法建立ws(但是可以登录)
        # while user.id in ping_uid_list:
        #     ping_uid_list.remove(user.id)
        return
