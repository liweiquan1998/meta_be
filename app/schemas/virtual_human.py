from typing import Union, List, Optional

from pydantic import BaseModel
from faker import Faker

faker = Faker(locale='zh_CN')

class VirtualHumanCheckName(BaseModel):
    id: Union[int, None] = None
    name: str

    class Config:
        schema_extra = {
            "example": {
                "name": faker.name()}}

class VirtualHumanCreate(BaseModel):
    name: str
    sex: int
    status: int = 1
    # creator_id: Optional[int] = None
    headimg_uri: str
    work_space: str

    class Config:
        schema_extra = {
            "example": {
                "name": faker.name(),
                "sex": faker.pyint(0, 1, 2),
                "status": faker.pyint(0, 1),
                "headimg_uri": "xxxx",
                "work_space": "xxxxxxxx"}}


class VirtualHumanUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[int] = None
    headimg_uri: Optional[str] = None
    work_space: Optional[str] = None


class VirtualHumanGet(BaseModel):
    creator_id: Optional[int] = None
    name: Union[str, None] = None
    sex: Union[int, None] = None


class VirtualHuman(BaseModel):
    id: int
    name: str
    sex: int
    status: int
    creator_id: int
    create_time: int
    heading_uri: str
    work_space: str

    class Config:
        orm_mode = True
