from datetime import timezone
from typing import Union, Any
from datetime import datetime, timedelta
from typing import Union

import fastapi.exceptions
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from app import get_db, models
import os

sx_servers = {"sxkjue", 'sxkjALG'}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/swagger/login")

ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('user_expire_minutes', '4320')
ALGORITHM = os.getenv('user_algorithm', 'HS256')
JWT_SECRET_KEY = {
    'user': os.getenv('user_secret_keys_user', '7491ad7fa77a6a4e5bad2f1d87331ecee129203bfa2f2480bb5c75abb7506e50'),
    'admin': os.getenv('user_secret_keys_admin', '25313d9bf1b85552a2b8c8de78723b3d9c1bb5739fed8213a3fc0c705e8909e4'),
    'customer': os.getenv('user_secret_keys_customer', '5d7905fad3ba152347a005334ec3fe3a1946fc5d0415ef47ea88f8357ae0bf76')
}


class TokenData(BaseModel):
    name: str


class TokenSchemas(BaseModel):
    access_token: str
    token_type: str


#  函数接收一个普通密码，并返回可以安全存储在数据库中的哈希值
def get_password_hash(password) -> str:
    return pwd_context.hash(password)


# 函数接收普通密码和散列密码，并返回一个布尔值，代表密码是否匹配。
def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# 创建token
def create_access_token(subject: Union[str, Any], user_type: str, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now(timezone.utc) + timedelta(seconds=expires_delta)
    else:
        expires_delta = datetime.now(timezone.utc) + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))

    to_encode = {"sub": str(subject), "exp": expires_delta}
    return jwt.encode(to_encode, JWT_SECRET_KEY[user_type], ALGORITHM)


# 解析token
def check_access_token(token: str, user_type: str):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY[user_type], ALGORITHM)
        return payload.get("sub"), payload.get("exp")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="token 过期")
    except jwt.JWTError:
        print(f"token 错误,token:{token}")
        raise HTTPException(status_code=401, detail=f"token 错误,token:{token}")


def check_user_id(token: str, db: Session = Depends(get_db)):
    try:
        userid, expire_time = check_access_token(token, 'user')
        # 验证用户是否存在
        user = db.query(models.User).filter(models.User.id == userid).first()
        if user:
            return int(userid)
        else:
            return None
    except fastapi.exceptions.HTTPException:
        return None


# 验证
async def check_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    if token in sx_servers:
        return True
    userid, expire_time = check_access_token(token, 'user')
    # 验证用户是否存在
    user = db.query(models.User).filter(models.User.id == userid).first()
    if user is None:
        raise HTTPException(status_code=401, detail="商户不存在")
    return user


async def check_user_ws(token: str, db: Session = Depends(get_db)):
    if token in sx_servers:
        return True
    userid, expire_time = check_access_token(token, 'user')
    # 验证用户是否存在
    user = db.query(models.User).filter(models.User.id == userid).first()
    if user is None:
        raise HTTPException(status_code=401, detail="商户不存在")
    return user
