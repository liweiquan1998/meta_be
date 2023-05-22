import time
from typing import Union

from pydantic import BaseModel
from faker import Faker

faker = Faker(locale='zh_CN')


class TTSCreate(BaseModel):
    text_content: Union[str] = None
    role: Union[int] = None

    class Config:
        schema_extra = {
            "example": {
                "text_content": faker.pystr(10),
                "role": 0
            }}


class TTS(BaseModel):
    id: int
    text_id: str
    text_content: str
    sex: int
    create_time: int
    update_time: int
    status: int
    config_uri: str
    role: int

    class Config:
        orm_mode = True
