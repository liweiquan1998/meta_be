from typing import Union

from pydantic import BaseModel
from faker import Faker

faker = Faker(locale='zh_CN')


class BackgroundImagesCreate(BaseModel):
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


class BackgroundImagesGet(BaseModel):
    name: Union[str, None] = None
    type: Union[int, None] = None


class BackgroundImages(BaseModel):
    id: int
    name: str
    type: int
    file_uri: str
    create_time: int
    creator_id: int

    class Config:
        orm_mode = True