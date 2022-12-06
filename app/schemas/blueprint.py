import time
from typing import Union

from pydantic import BaseModel
from faker import Faker

faker = Faker(locale='zh_CN')


class BlueprintCreate(BaseModel):
    store_id: int
    creator_id: Union[int] = None
    config_uri: Union[str] = None

    class Config:
        schema_extra = {
            "example": {
                "store_id": faker.pyint(1, 10),
                "creator_id": faker.pyint(1, 100),
                "config_uri": ""
            }}


class BlueprintUpdate(BaseModel):
    config_uri: Union[str] = None

    class Config:
        schema_extra = {
            "example": {
                "config_uri": ""
            }}


class Blueprint(BaseModel):
    id: int
    store_id: int
    creator_id: int
    config_uri: str
    create_time: int
    update_time: int

    class Config:
        orm_mode = True
