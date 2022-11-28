from typing import Union

from pydantic import BaseModel
from faker import Faker

faker = Faker(locale='zh_CN')

class VirtualHumanCreate(BaseModel):
    name: str
    sex: str
