import random
from typing import Union

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
