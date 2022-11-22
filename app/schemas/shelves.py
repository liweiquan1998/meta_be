from typing import Union

from pydantic import BaseModel
from faker import Faker

faker = Faker(locale='zh_CN')


class ShelvesCreate(BaseModel):
    scene_id: int
    config: str

    class Config:
        schema_extra = {
            "example": {
                "scene_id": faker.pyint(1, 8),
                "config": "xxxx"}}


class ShelvesUpdate(BaseModel):
    config: str


class ShelvesGet(BaseModel):
    scene_id: Union[int, None] = None


class Shelves(BaseModel):
    id: int
    scene_id: int
    config: str

    class Config:
        schema_extra = {
            "example": {
                "id": faker.pyint(1, 8),
                "scene_id": faker.pyint(1, 8),
                "config": "xxxx"}}
