import random
from typing import Union
from fastapi import Query
from pydantic import BaseModel
from faker import Faker

faker = Faker(locale='zh_CN')

class SceneBase(BaseModel):
    # 场景名称
    name: str = Query(default=..., min_length=1, max_length=50)
    # 缩略图
    thumbnail: str = Query(default=..., min_length=1, max_length=255)
    # 配置文件
    config_file: str = Query(default=..., min_length=1, max_length=255)
    # 标签（0：all，1：元商店，2：直播）
    tag: int = Query(default=..., ge=0, le=2)
    # 阶段（0：硬装，1：软装，2：应用）
    stage: int = Query(default=..., ge=0, le=2)
    # 基础场景id
    base_id: int
    # 商店id
    store_id: Union[int, None]

class SceneCreate(SceneBase):
    class Config:
        schema_extra = {
            "example": {
                "name": f"{faker.company_prefix()}的场景",
                "thumbnail": '/file/nfs/SceneAssets/2A0206964478EFE72AF8F3B0260C66D8.png',
                "config_file": '/file/nfs/SceneAssets/202212/1669986425',
                "tag": random.choice([0, 1, 2]),  # 0: all 1:直播 2:商铺
                "stage": random.choice([0, 1, 2]),  # 0:硬装 1:软装 2:应用
                "base_id": 1,  # 基础场景id
                "store_id": 1,  # 商店id
            }
        }


class SceneGet(BaseModel):
    name: Union[str, None] = None
    tag: Union[int, None] = Query(default=None, ge=0, le=2)
    stage: int = Query(default=..., ge=0, le=2)


class SceneUpdate(SceneBase):

    class Config:
        schema_extra = {
            "example": {
                "name": f"{faker.company_prefix()}的场景",
                "thumbnail": '/file/nfs/SceneAssets/2A0206964478EFE72AF8F3B0260C66D8.png',
                "config_file": '/file/nfs/SceneAssets/202212/1669986425',
                "tag": random.choice([0, 1, 2]),  # 0: all 1:直播 2:商铺
                "stage": random.choice([0, 1, 2]),  # 0:硬装 1:软装 2:应用
                "base_id": 1,  # 基础场景id
                "store_id": 1,  # 商店id
            }
        }


class Scene(SceneBase):
    # 场景id
    id: int
    # 创建者id
    create_id: int
    # 创建时间
    create_time: int
    # 更新者id
    update_id: int
    # 更新时间
    update_time: int

    class Config:
        orm_mode = True
