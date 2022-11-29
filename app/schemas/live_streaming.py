# sourcery skip: remove-redundant-slice-index
from typing import Union, List, Optional

from pydantic import BaseModel
from faker import Faker

faker = Faker(locale='zh_CN')

class LiveStreamingCreate(BaseModel):
    name: str
    address: str
    status: int
    work_space: str
    virtual_human_id: int
    special_effects_id: int
    background_id: int
    creator_id: int
    live_account_id: int

    class Config:
        schema_extra = {
            "example": {
                "name": faker.name(),
                "address": faker.uri(),
                "status": 0,
                "work_space": faker.md5()[0:10],
                "virtual_human_id": faker.pyint(5, 10),
                "special_effects_id": faker.pyint(5, 10),
                "background_id": faker.pyint(5, 10),
                "creator_id": faker.pyint(5, 10),
                "live_account_id": faker.pyint(5, 10)}
            }

class LiveStreamingUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    status: Optional[int] = None
    work_space: Optional[str] = None
    virtual_human_id: Optional[int] = None
    special_effects_id: Optional[int] = None
    background_id: Optional[int] = None
    live_account_id: Optional[int] = None

    class Config:
        schema_extra = {
            "example": {
                "name": faker.name(),
                "address": faker.uri(),
                "status": 1,
                "work_space": faker.md5()[0:10],
                "virtual_human_id": faker.pyint(5, 10),
                "special_effects_id": faker.pyint(5, 10),
                "background_id": faker.pyint(5, 10),
                "live_account_id": faker.pyint(5, 10)},
        }

class LiveStreamingGet(BaseModel):
    name: Optional[str] = None
    create_time: Optional[int] = None
    status: Optional[int] = None

class LiveStreaming(BaseModel):
    id: int
    name: str
    address: str
    status: int
    work_space: str
    virtual_human_id: int
    special_effects_id: int
    background_id: int
    creator_id: int
    live_account_id: int
    create_time: int

    class Config:
        orm_mode = True
