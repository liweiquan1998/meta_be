import time
from typing import Union, Optional

from pydantic import BaseModel
from faker import Faker

faker = Faker(locale='zh_CN')


class MetaObjCreateBase(BaseModel):
    name: str
    type: int
    kind: int
    creator_id: int
    height: int


class MetaObjByImageCreate(MetaObjCreateBase):
    aigc: str
    status: int

    class Config:
        schema_extra = {
            "example": {
                "name": f"{faker.company_prefix()}的商品",
                "type": 1,
                "kind": 1,
                "aigc": "xxx,xxx,xxx",
                "status": 0,
                "creator_id": faker.pyint(1, 10),
                "height": faker.pyint(1, 100)
            }}


class MetaObjByVideoCreate(MetaObjCreateBase):
    aigc: str
    status: int

    class Config:
        schema_extra = {
            "example": {
                "name": f"{faker.company_prefix()}的商品",
                "type": 1,
                "kind": 1,
                "aigc": "xxxxx",
                "status": 0,
                "creator_id": faker.pyint(1, 10),
                "height": faker.pyint(1, 100)
            }}


class MetaObjByModelCreate(MetaObjCreateBase):
    model: str
    thumbnail: str
    tag: str

    class Config:
        schema_extra = {
            "example": {
                "name": f"{faker.company_prefix()}的摆放物品",
                "type": 0,
                "kind": 0,
                "model": "xxxxx",
                "thumbnail": "xxxxx",
                "tag": "桌子",
                "creator_id": faker.pyint(1, 10),
                "height": faker.pyint(1, 100)
            }}


class MetaObjUpdate(BaseModel):
    status: Optional[int] = None
    model: Optional[str] = None
    thumbnail: Optional[str] = None




class MetaObjGet(BaseModel):
    name: Union[str, None] = None
    type: Union[int, None] = None
    kind: Union[int, None] = None
    create_time: Union[int, None] = None
    status: Union[int, None] = None
    tag: Union[str, None] = None
    creator_id: Union[int,None] = None


class MetaObj(BaseModel):
    id: int
    name: str
    type: int
    kind: int
    aigc: str
    model: str
    thumbnail: str
    create_time: int
    status: int
    tag: str
    creator_id: int
    height: int

    class Config:
        orm_mode = True
