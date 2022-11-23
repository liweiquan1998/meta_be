import time
from typing import Union

from pydantic import BaseModel
from faker import Faker

faker = Faker(locale='zh_CN')


class StoreCreate(BaseModel):
    name: str
    scene_id: int
    thumbnail: str
    config: str
    creator_id: int

    class Config:
        schema_extra = {
            "example": {
                "name": f"{faker.company_prefix()}的商铺",
                "scene_id": faker.pyint(1, 8),
                "thumbnail": "xxxx",
                "config": "xxxx",
                "creator_id": faker.pyint(1, 10),
            }}


class StoreUpdate(BaseModel):
    name: str
    thumbnail: str
    config: str

    class Config:
        schema_extra = {
            "example": {
                "name": f"{faker.company_prefix()}的商铺",
                "thumbnail": "xxxx",
                "config": "xxxx",
            }}


class StoreGet(BaseModel):
    name: Union[str, None] = None


class Store(BaseModel):
    id: int
    name: str
    scene_id: int
    thumbnail: str
    config: str
    creator_id: int
    create_time: int

    class Config:
        orm_mode = True
