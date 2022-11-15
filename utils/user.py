from passlib.context import CryptContext
import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


#  函数接收一个普通密码，并返回可以安全存储在数据库中的哈希值
def get_password_hash(password) -> str:
    return pwd_context.hash(password)


# 函数接收普通密码和散列密码，并返回一个布尔值，代表密码是否匹配。
def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 3  # 3 day
ALGORITHM = "HS256"
JWT_SECRET_KEY = '\xc7\xab\30VV\xa4\r\xed\xac\x94u\xfd\xfaTU\x15&\xcc\x80\xc20\xees\xf4'  # should be kept secret
JWT_REFRESH_SECRET_KEY = '\xd00J\xd0*8/\xb2\xbfP\x88\xd4\x84\xa7u/\x9f<\xf00\x9cO\x8a'  # should be kept secret


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt
