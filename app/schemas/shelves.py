from typing import Union

from pydantic import BaseModel
from faker import Faker

faker = Faker(locale='zh_CN')


class ShelvesCreate(BaseModel):
    scene_id: int
    data: str
    shelf_id: str

    class Config:
        schema_extra = {
            "example": {
                "scene_id": faker.pyint(1, 8),
                "data": "xxxx",
                "shelf_id": "xxxxx"}}


class ShelvesUpdate(BaseModel):
    data: str


class ShelvesGet(BaseModel):
    scene_id: Union[int, None] = None


class Shelves(BaseModel):
    id: int
    scene_id: int
    shelf_id: str
    data: str

    class Config:
        orm_mode = True
