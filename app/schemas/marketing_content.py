from typing import Union, List, Optional

from pydantic import BaseModel
from faker import Faker

faker = Faker(locale='zh_CN')


class MarketingContentCreate(BaseModel):
    name: str
    content: str
    metaobj_id: int
    virtual_human_sex: int
    # creator_id: int
    # virtual_human_id: int
    # work_space: str

    class Config:
        schema_extra = {
            "example": {
                "name": "内容营销测试",
                "content": faker.text(),
                "metaobj_id": 1,
                "virtual_human_sex": faker.pyint(1, 2)}}


class ComposeVideo(BaseModel):
    marketing_content_id: int
    video_uri: str


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
