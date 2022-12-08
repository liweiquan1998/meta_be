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
    sku_ids: Union[str] = None

    class Config:
        schema_extra = {
            "example": {
                "name": f"{faker.company_prefix()}的商铺",
                "scene_id": faker.pyint(1, 8),
                "thumbnail": "xxxx",
                "config": "xxxx",
                "creator_id": faker.pyint(1, 10),
                "sku_ids": str([faker.pyint(1, 20) for i in range(5)])
            }}


class StoreUpdate(BaseModel):
    name: Union[str] = None
    thumbnail: Union[str] = None
    config: Union[str] = None
    sku_ids: Union[str] = None

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
    creator_name: str

    class Config:
        orm_mode = True
