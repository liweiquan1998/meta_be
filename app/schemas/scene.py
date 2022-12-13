import random
from typing import Union

from pydantic import BaseModel
from faker import Faker

faker = Faker(locale='zh_CN')


class SceneCreate(BaseModel):
    name: str
    tag: int
    base_id: int
    thumbnail: str
    config: str
    creator_id: int

    class Config:
        schema_extra = {
            "example": {
                "name": f"{faker.company_prefix()}的场景",
                "tag": random.choice([1, 2]),  # 1:直播 2:商铺
                "base_id": random.choice([1, 2, 3]),  # 基础场景id
                "thumbnail": 'SceneAssets/202211',
                "config": 'SceneAssets/202211',
                "creator_id": faker.pyint(5, 10)}
        }


class SceneGet(BaseModel):
    creator_id: Union[int, None] = None
    name: Union[str, None] = None
    tag: Union[int, None] = None
    base_id: Union[int, None] = None


class SceneUpdate(BaseModel):
    name: str
    thumbnail: str
    config: str


class Scene(BaseModel):
    id: int
    name: str
    tag: int
    base_id: int
    thumbnail: str
    config: str
    create_time: int
    update_time: int
    creator_id: int
    create_time: int

    class Config:
        orm_mode = True
