from typing import Union

from pydantic import BaseModel
from faker import Faker

faker = Faker(locale='zh_CN')


class BackgroundCreate(BaseModel):
    name: str
    type: int
    file_uri: str
    creator_id: int

    class Config:
        schema_extra = {
            "example": {
                "name": f"{faker.pystr()}背景",
                "type": faker.pyint(0, 1),
                "file_uri": 'xxxx',
                "creator_id": faker.pyint(5, 10)}
        }

class BackgroundUpdate(BaseModel):
    name: Union[str, None] = None
    type: Union[int, None] = None
    file_uri: Union[str, None] = None

    class Config:
        schema_extra = {
            "example": {
                "name": f"{faker.pystr()}背景",
                "type": faker.pyint(0, 1),
                "file_uri": 'xxxx'}
        }


class BackgroundGet(BaseModel):
    name: Union[str, None] = None
    type: Union[int, None] = None


class Background(BaseModel):
    id: int
    name: str
    type: int
    file_uri: str
    create_time: int
    creator_id: int

    class Config:
        orm_mode = True