from typing import Union

from pydantic import BaseModel
from faker import Faker

faker = Faker(locale='zh_CN')


class VirtualHumanCreate(BaseModel):
    name: str
    sex: int
    status: int
    creator_id: int
    headimg_uri: str
    work_space: str

    class Config:
        schema_extra = {
            "example": {
                "name": faker.name(),
                "sex": faker.pyint(0, 1, 2),
                "status": faker.pyint(0, 1),
                "creator_id": faker.pyint(50, 100),
                "headimg_uri": "xxxx",
                "work_space": "xxxxxxxx"}}


class VirtualHumanUpdate(BaseModel):
    name: str
    status: int
    headimg_uri: str
    work_space: str


class VirtualHumanGet(BaseModel):
    name: Union[str, None] = None
    sex: Union[int, None] = None


class VirtualHuman(BaseModel):
    id: int
    name: str
    sex: int
    status: int
    creator_id: int
    create_time: int
    headimg_uri: str
    work_space: str

    class Config:
        orm_mode = True
