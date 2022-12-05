# sourcery skip: remove-redundant-slice-index
from typing import Union, List, Optional

from pydantic import BaseModel
from faker import Faker

faker = Faker(locale='zh_CN')


class LiveAccountCreate(BaseModel):
    name: str
    address: str
    platform: str
    key: str
    token: str
    creator_id: Union[int] = None

    class Config:
        schema_extra = {
            "example": {
                "name": faker.name(),
                "address": faker.uri(),
                "platform": '抖音',
                "key": faker.md5()[0:10],
                "token": faker.md5()[0:10],
                "creator_id": faker.pyint(5, 10)}
            }


class LiveAccountUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    platform: Optional[str] = None
    key: Optional[str] = None
    token: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "name": faker.name(),
                "address": faker.uri(),
                "platform": 'B站',
                "key": faker.md5()[0:10],
                "token": faker.md5()[0:10]},
        }


class LiveAccountGet(BaseModel):
    name: Optional[str] = None


class LiveAccount(BaseModel):
    id: int
    name: str
    address: str
    platform: str
    key: str
    token: str
    last_time: int
    creator_id: int

    class Config:
        orm_mode = True
