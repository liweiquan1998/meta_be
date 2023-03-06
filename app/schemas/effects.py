import random
from typing import Union, Optional

from pydantic import BaseModel
from faker import Faker


class EffectCreate(BaseModel):
    name: str
    pkg: str
    thumbnail: str

    class Config:
        schema_extra = {
            "example": {
                "name": "爆炸",
                "pkg": "SceneAssets/202211",
                "thumbnail": "SceneAssets/202211"
            }}


class EffectGet(BaseModel):
    name: Union[str, None] = None
    create_time: Union[int, None] = None
