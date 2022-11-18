import random
from typing import Union

from pydantic import BaseModel
from faker import Faker

faker = Faker(locale='zh_CN')

class SceneBaseGet(BaseModel):
    name: Union[str, None] = None


class SceneBase(BaseModel):
    id: int
    name: str
    thumbnail: str

    class Config:
        orm_mode = True
