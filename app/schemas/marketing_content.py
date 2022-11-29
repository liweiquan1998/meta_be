from typing import Union, List, Optional

from pydantic import BaseModel
from faker import Faker

faker = Faker(locale='zh_CN')


class MarketingContentCreate(BaseModel):
    name: str
    content: str
    metaobj_id: int
    creator_id: int
    virtual_human_id: int
    work_space: str

    class Config:
        schema_extra = {
            "example": {
                "name": faker.name(),
                "content": faker.text(),
                "metaobj_id": faker.pyint(5, 10),
                "creator_id": faker.pyint(5, 10),
                "virtual_human_id": faker.pyint(5, 10),
                "work_space": faker.address()}}


class MarketingContentUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[int] = None
    content: Optional[str] = None
    metaobj_id: Optional[int] = None
    work_space: Optional[str] = None
    audio_uri: Optional[str] = None
    video_uri: Optional[str] = None


class MarketingContentGet(BaseModel):
    name: Optional[str] = None
    status:  Optional[int] = None
    create_time:  Optional[int] = None


class MarketingContent(BaseModel):
    id: int
    name: str
    content: str
    metaobj_id: int
    creator_id: int
    virtual_human_id: int
    create_time: int
    status: int
    audio_uri: str
    video_uri: str
    work_space: str

    class Config:
        orm_mode = True
