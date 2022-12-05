import random
from typing import Union
from fastapi_pagination import Params
from pydantic import BaseModel
from faker import Faker

faker = Faker(locale='zh_CN')


class ApparelBase(BaseModel):
    work_space: Union[str] = None
    apparel_name: Union[str] = None
    apparel_type: Union[int] = None
    thumbnail: Union[str] = None
    file_uri: Union[str] = None


class ApparelCreate(ApparelBase):
    work_space: Union[str] = None
    apparel_name: Union[str] = None
    apparel_type: Union[int] = None
    thumbnail: Union[str] = None
    file_uri: Union[str] = None


class ApparelParams(Params):
    apparel_name: Union[str] = None
    apparel_type: Union[str] = None


class ApparelUpdate(ApparelBase):
    pass


class Apparel(ApparelBase):
    id: int

    class Config:
        orm_mode = True
