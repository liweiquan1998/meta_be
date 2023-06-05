import time
from typing import Union

from pydantic import BaseModel
from faker import Faker

faker = Faker(locale='zh_CN')


class BlueprintCreate(BaseModel):
    store_id: int
    creator_id: Union[int] = None
    graphdata: Union[str] = None
    nodedata: Union[str] = None
    uedata: Union[str] = None

    class Config:
        schema_extra = {
            "example": {
                "store_id": faker.pyint(1, 10),
                "creator_id": faker.pyint(1, 100),
                "graphdata": "",
                "nodedata": "",
                "uedata": "",
            }}


class BlueprintUpdate(BaseModel):
    graphdata: Union[str] = None
    nodedata: Union[str] = None
    uedata: Union[str] = None

    class Config:
        schema_extra = {
            "example": {
                "graphdata": "",
                "nodedata": "",
                "uedata": "",
            }}


class Blueprint(BaseModel):
    id: int
    store_id: int
    creator_id: int
    create_time: int
    update_time: int
    graphdata: str
    nodedata: str
    uedata: str

    class Config:
        orm_mode = True
