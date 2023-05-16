import time
from typing import Union, Optional

from pydantic import BaseModel
from faker import Faker

faker = Faker(locale='zh_CN')

class MetaObjCreate(BaseModel):
    name: str
    type: int
    kind: int
    aigc: Optional[list] = None

    model: Optional[str] = None
    thumbnail: Optional[str] = None
    ue_address: Optional[str] = None
    fbx_id: Optional[str] = None
    tag: Optional[str] = None

    height: Optional[float] = None

    class Config:
        schema_extra = {
            "example": {
                "name": f"{faker.company_prefix()}的商品【必填 str】",
                "type": "0: upload model 1: image 2: video【必填 int！】 ",
                "kind": "0:场景素材 1:商品【必填 int！】",
                "aigc": [
                    "202212/64d0c86a-7515-11ed-8267-0242ac1a0002.png",
                    "202212/64f38abc-7515-11ed-8267-0242ac1a0002.png",
                    "202212/6516504c-7515-11ed-8267-0242ac1a0002.png",
                    '渲染模型时【选填】'
                ],
                'model': '上传模型时【选填 str】',
                'thumbnail': '上传模型时【选填 str】',
                'ue_address': '转换fbx文件时【选填 str】',
                'fbx_id': '转换fbx文件时【选填 str】',
                'tag': '上模型时【选填 str】',
                'height': '【选填 float】',
            },
            "example2": {
                "name": f"{faker.company_prefix()}的商品【必填 str】"
            }
        }


class MetaObjCreateBase(BaseModel):
    name: str
    type: int
    kind: int
    height: Optional[int] = None


class MetaObjByImageCreate(BaseModel):
    name: str
    type: int = 1
    aigc: list
    height: Optional[int] = None
    kind: Optional[int] = 1
    thumbnail: Optional[str] = None
    ue_address: Optional[str] = None
    fbx_id: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "name": f"{faker.company_prefix()}的商品",
                "type": 1,
                "aigc": [
                    "202212/50fa1a9e-7515-11ed-8267-0242ac1a0002.png",
                    "202212/51388c84-7515-11ed-8267-0242ac1a0002.png",
                    "202212/51771f12-7515-11ed-8267-0242ac1a0002.png",
                    "202212/51a52e20-7515-11ed-8267-0242ac1a0002.png",
                    "202212/51ecd32e-7515-11ed-8267-0242ac1a0002.png",
                    "202212/5233980e-7515-11ed-8267-0242ac1a0002.png",
                    "202212/526dbf52-7515-11ed-8267-0242ac1a0002.png",
                    "202212/52d25cbe-7515-11ed-8267-0242ac1a0002.png",
                    "202212/5304b7ea-7515-11ed-8267-0242ac1a0002.png",
                    "202212/53381ad6-7515-11ed-8267-0242ac1a0002.png",
                    "202212/537337e2-7515-11ed-8267-0242ac1a0002.png",
                    "202212/53c88fee-7515-11ed-8267-0242ac1a0002.png",
                    "202212/54117e8e-7515-11ed-8267-0242ac1a0002.png",
                    "202212/54650b76-7515-11ed-8267-0242ac1a0002.png",
                    "202212/54b34ce6-7515-11ed-8267-0242ac1a0002.png",
                    "202212/54ecf78e-7515-11ed-8267-0242ac1a0002.png",
                    "202212/555a98fc-7515-11ed-8267-0242ac1a0002.png",
                    "202212/55aac71e-7515-11ed-8267-0242ac1a0002.png",
                    "202212/55dff3ee-7515-11ed-8267-0242ac1a0002.png",
                    "202212/563fc71a-7515-11ed-8267-0242ac1a0002.png",
                    "202212/566dac66-7515-11ed-8267-0242ac1a0002.png",
                    "202212/56a6fbb0-7515-11ed-8267-0242ac1a0002.png",
                    "202212/56e5b828-7515-11ed-8267-0242ac1a0002.png",
                    "202212/5728980a-7515-11ed-8267-0242ac1a0002.png",
                    "202212/579327ce-7515-11ed-8267-0242ac1a0002.png",
                    "202212/57c89648-7515-11ed-8267-0242ac1a0002.png",
                    "202212/58112156-7515-11ed-8267-0242ac1a0002.png",
                    "202212/5852593c-7515-11ed-8267-0242ac1a0002.png",
                    "202212/58850bca-7515-11ed-8267-0242ac1a0002.png",
                    "202212/58c76ea2-7515-11ed-8267-0242ac1a0002.png",
                    "202212/58fec1b8-7515-11ed-8267-0242ac1a0002.png",
                    "202212/593df554-7515-11ed-8267-0242ac1a0002.png",
                    "202212/5964fcbc-7515-11ed-8267-0242ac1a0002.png",
                    "202212/599b31d8-7515-11ed-8267-0242ac1a0002.png",
                    "202212/59c6b6b4-7515-11ed-8267-0242ac1a0002.png",
                    "202212/59faa94c-7515-11ed-8267-0242ac1a0002.png",
                    "202212/5a277c60-7515-11ed-8267-0242ac1a0002.png",
                    "202212/5a4ba6ee-7515-11ed-8267-0242ac1a0002.png",
                    "202212/5a7535ea-7515-11ed-8267-0242ac1a0002.png",
                    "202212/5a9d5b6a-7515-11ed-8267-0242ac1a0002.png",
                    "202212/5ace42ac-7515-11ed-8267-0242ac1a0002.png",
                    "202212/5b0fadbe-7515-11ed-8267-0242ac1a0002.png",
                    "202212/5b41ebf8-7515-11ed-8267-0242ac1a0002.png",
                    "202212/5b86b3e6-7515-11ed-8267-0242ac1a0002.png",
                    "202212/5bc264ae-7515-11ed-8267-0242ac1a0002.png",
                    "202212/5c02528a-7515-11ed-8267-0242ac1a0002.png",
                    "202212/5c3ef62c-7515-11ed-8267-0242ac1a0002.png",
                    "202212/5c809cb2-7515-11ed-8267-0242ac1a0002.png",
                    "202212/5ccf49de-7515-11ed-8267-0242ac1a0002.png",
                    "202212/5d090fa2-7515-11ed-8267-0242ac1a0002.png",
                    "202212/5d72566a-7515-11ed-8267-0242ac1a0002.png",
                    "202212/5dd260c8-7515-11ed-8267-0242ac1a0002.png",
                    "202212/5e084ef4-7515-11ed-8267-0242ac1a0002.png",
                    "202212/5e36d634-7515-11ed-8267-0242ac1a0002.png",
                    "202212/5e5aae88-7515-11ed-8267-0242ac1a0002.png",
                    "202212/5e87b036-7515-11ed-8267-0242ac1a0002.png",
                    "202212/5eafa5b4-7515-11ed-8267-0242ac1a0002.png",
                    "202212/5ed3a4c8-7515-11ed-8267-0242ac1a0002.png",
                    "202212/5efd75aa-7515-11ed-8267-0242ac1a0002.png",
                    "202212/5f280f22-7515-11ed-8267-0242ac1a0002.png",
                    "202212/5f4fe984-7515-11ed-8267-0242ac1a0002.png",
                    "202212/5f8aae52-7515-11ed-8267-0242ac1a0002.png",
                    "202212/5fb2c3ec-7515-11ed-8267-0242ac1a0002.png",
                    "202212/5fd60122-7515-11ed-8267-0242ac1a0002.png",
                    "202212/5ffcdfd6-7515-11ed-8267-0242ac1a0002.png",
                    "202212/60245c96-7515-11ed-8267-0242ac1a0002.png",
                    "202212/604d7db0-7515-11ed-8267-0242ac1a0002.png",
                    "202212/607650fa-7515-11ed-8267-0242ac1a0002.png",
                    "202212/609941b4-7515-11ed-8267-0242ac1a0002.png",
                    "202212/60bef864-7515-11ed-8267-0242ac1a0002.png",
                    "202212/60e12b3c-7515-11ed-8267-0242ac1a0002.png",
                    "202212/610d71a6-7515-11ed-8267-0242ac1a0002.png",
                    "202212/6135749e-7515-11ed-8267-0242ac1a0002.png",
                    "202212/6159d60e-7515-11ed-8267-0242ac1a0002.png",
                    "202212/617d8770-7515-11ed-8267-0242ac1a0002.png",
                    "202212/61a1740a-7515-11ed-8267-0242ac1a0002.png",
                    "202212/61db376c-7515-11ed-8267-0242ac1a0002.png",
                    "202212/62095156-7515-11ed-8267-0242ac1a0002.png",
                    "202212/622ab8aa-7515-11ed-8267-0242ac1a0002.png",
                    "202212/624a4576-7515-11ed-8267-0242ac1a0002.png",
                    "202212/626a7332-7515-11ed-8267-0242ac1a0002.png",
                    "202212/628b7ad2-7515-11ed-8267-0242ac1a0002.png",
                    "202212/62b2eab8-7515-11ed-8267-0242ac1a0002.png",
                    "202212/62d5c128-7515-11ed-8267-0242ac1a0002.png",
                    "202212/6305cbca-7515-11ed-8267-0242ac1a0002.png",
                    "202212/6328f7b2-7515-11ed-8267-0242ac1a0002.png",
                    "202212/634b4efc-7515-11ed-8267-0242ac1a0002.png",
                    "202212/636a5766-7515-11ed-8267-0242ac1a0002.png",
                    "202212/638e185e-7515-11ed-8267-0242ac1a0002.png",
                    "202212/63b6468a-7515-11ed-8267-0242ac1a0002.png",
                    "202212/63d56146-7515-11ed-8267-0242ac1a0002.png",
                    "202212/63f80bb0-7515-11ed-8267-0242ac1a0002.png",
                    "202212/64193902-7515-11ed-8267-0242ac1a0002.png",
                    "202212/643b832c-7515-11ed-8267-0242ac1a0002.png",
                    "202212/645e4c5e-7515-11ed-8267-0242ac1a0002.png",
                    "202212/6487dba0-7515-11ed-8267-0242ac1a0002.png",
                    "202212/64aadee8-7515-11ed-8267-0242ac1a0002.png",
                    "202212/64d0c86a-7515-11ed-8267-0242ac1a0002.png",
                    "202212/64f38abc-7515-11ed-8267-0242ac1a0002.png",
                    "202212/6516504c-7515-11ed-8267-0242ac1a0002.png"
                ],
            }}


class MetaObjByVideoCreate(BaseModel):
    name: str
    type: int = 1
    aigc: list
    height: Optional[int] = None
    kind: Optional[int] = 1
    thumbnail: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "name": f"{faker.company_prefix()}的商品",
                "type": 1,
                "aigc": ["202212/1670312821.mp4"],
            }}


class MetaObjByModelCreate(MetaObjCreateBase):
    model: str
    thumbnail: str
    kind: Optional[int] = 1
    type: int = 0

    class Config:
        schema_extra = {
            "example": {
                "name": f"{faker.company_prefix()}的摆放物品",
                "type": 0,
                "kind": 0,
                "model": "xxxxx",
                "thumbnail": "xxxxx",

                "tag": "桌子",
                "creator_id": faker.pyint(1, 10),
                "height": faker.pyint(1, 100)
            }}


class MetaObjUpdate(BaseModel):
    status: Optional[int] = None
    model: Optional[str] = None
    thumbnail: Optional[str] = None
    ue_address: Optional[str] = None
    fbx_id: Optional[str] = None


class MetaObjGet(BaseModel):
    name: Union[str, None] = None
    type: Union[int, None] = None
    kind: Union[int, None] = None
    create_time: Union[int, None] = None
    status: Union[int, None] = None
    tag: Union[str, None] = None
    creator_id: Union[int, None] = None
    ue_address: Union[str, None] = None
    fbx_id: Optional[str] = None


class MetaObj(BaseModel):
    id: int
    name: str
    type: int
    kind: int
    aigc: str
    model: str
    thumbnail: str
    create_time: int
    status: int
    tag: str
    creator_id: int
    height: float
    ue_address: str
    fbx_id: str

    class Config:
        orm_mode = True
