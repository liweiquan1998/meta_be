import time
from typing import Union

from pydantic import BaseModel
from faker import Faker

faker = Faker(locale='zh_CN')


class TTSCreate(BaseModel):
    blueprint_id: Union[int] = None
    pop_id: Union[int] = None
    status: Union[int] = None
    config_uri: Union[str] = None

    class Config:
        schema_extra = {
            "example": {
                "blueprint_id": faker.pyint(1, 10),
                "pop_id": faker.pyint(1, 100),
                "status": faker.pyint(1, 10),
                "config_uri": "",
            }}


class TTSUpdate(BaseModel):
    id: Union[int] = None
    blueprint_id: Union[int] = None
    pop_id: Union[int] = None
    status: Union[int] = None
    config_uri: Union[str] = None

    class Config:
        schema_extra = {
            "example": {
                "id": faker.pyint(1, 10),
                "blueprint_id": faker.pyint(1, 10),
                "pop_id": faker.pyint(1, 100),
                "status": faker.pyint(1, 10),
                "config_uri": "",
            }}


class TTS(BaseModel):
    id: int
    blueprint_id: int
    pop_id: int
    create_time: int
    update_time: int
    status: int
    config_uri: str

    class Config:
        orm_mode = True
