# sourcery skip: remove-redundant-slice-index
from typing import Union, List, Optional
from pydantic import BaseModel
from faker import Faker

faker = Faker(locale='zh_CN')


class LiveStreamingCreate(BaseModel):
    name: str
    status: int = 0
    virtual_human_id: int
    base_scene_id: int
    live_account_id: int

    class Config:
        schema_extra = {
            "example": {
                "name": faker.name(),
                "base_scene_id": faker.pyint(5, 10),
                "live_account_id": faker.pyint(5, 10),
                "virtual_human_id": faker.pyint(1, 5)}
            }


class LiveStreamingUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    status: Optional[int] = None
    virtual_human_id: Optional[int] = None
    base_scene_id: Optional[int] = None
    live_account_id: Optional[int] = None
    config: Optional[str] = None
    last_update: Optional[int] = None

    class Config:
        schema_extra = {
            "example": {
                "name": faker.name(),
                "address": faker.uri(),
                "status": 1,
                "virtual_human_id": faker.pyint(5, 10),
                "base_scene_id": faker.pyint(5, 10),
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
