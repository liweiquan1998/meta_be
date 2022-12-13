from typing import Union,Optional

from pydantic import BaseModel
from faker import Faker

faker = Faker(locale='zh_CN')


class UserBase(BaseModel):
    storename: str


class UserCreate(UserBase):
    name: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "storename": f"{faker.company_prefix()}元宇宙旗舰店",
                "name": faker.name(),
                "password": faker.password()}}


class UserUpdate(UserBase):
    name: Optional[str] = None
    password: Optional[str] = None
    status: Optional[int] = None
    occupied: Optional[int] = None


class UserGet(UserBase):
    storename: Union[str, None] = None
    create_time: Union[int, None] = None
    last_login: Union[int, None] = None
    status: Union[int, None] = None


class UserLogin(BaseModel):
    name: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "name": faker.name(),
                "password": faker.password()}}


class User(UserBase):
    id: int
    storename: str
    status: int
    name: str
    password: str
    auth_token: str
    create_time: int
    update_time: int
    last_login: int

    class Config:
        orm_mode = True
