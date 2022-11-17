import time

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
from datetime import datetime, timedelta
from typing import Union
from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from app import get_db
# 密码
import app.crud as crud
from utils import web_try

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


#  函数接收一个普通密码，并返回可以安全存储在数据库中的哈希值
def get_password_hash(password) -> str:
    return pwd_context.hash(password)


# 函数接收普通密码和散列密码，并返回一个布尔值，代表密码是否匹配。
def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 3  # 3 day
ALGORITHM = "HS256"
JWT_SECRET_KEY = {
    "user": "7491ad7fa77a6a4e5bad2f1d87331ecee129203bfa2f2480bb5c75abb7506e50",
    "admin": "25313d9bf1b85552a2b8c8de78723b3d9c1bb5739fed8213a3fc0c705e8909e4",
    "customer": '5d7905fad3ba152347a005334ec3fe3a1946fc5d0415ef47ea88f8357ae0bf76'
}


class TokenData(BaseModel):
    username: str


class TokenSchemas(BaseModel):
    access_token: str
    token_type: str


# credentials_exception = HTTPException(
#     status_code=status.HTTP_401_UNAUTHORIZED,
#     detail="Could not validate credentials",
#     headers={"WWW-Authenticate": "Bearer"},
# )

# 创建token
def create_access_token(subject: Union[str, Any], user_type: str, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + timedelta(seconds=expires_delta)
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"sub": str(subject), "exp": expires_delta}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY[user_type], ALGORITHM)
    return encoded_jwt


# 解析token
def check_access_token(token: str, user_type: str):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY[user_type], ALGORITHM)
        return payload.get("sub"), payload.get("exp")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="token 过期")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="token 错误")


# 验证
async def check_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    username, expire_time = check_access_token(token, 'user')
    # 验证用户是否存在
    user = crud.get_user_once_by_username(db, username)
    if user is None:
        raise HTTPException(status_code=401, detail="商户不存在")
    return user


async def check_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    username, expire_time = check_access_token(token, 'admin')
    # 验证用户是否存在
    user = crud.get_admin_once_by_username(db, username)
    if user is None:
        raise HTTPException(status_code=401, detail="超管不存在")
    return user


async def check_customer(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    username, expire_time = check_access_token(token, 'customer')
    # 验证用户是否存在
    user = crud.get_customer_once_by_username(db, username)
    if user is None:
        raise HTTPException(status_code=401, detail="用户不存在")
    return user
