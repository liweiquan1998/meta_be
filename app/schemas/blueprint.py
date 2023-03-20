import time
from typing import Union

from pydantic import BaseModel
from faker import Faker

faker = Faker(locale='zh_CN')


class BlueprintCreate(BaseModel):
    store_id: int
    creator_id: Union[int] = None
    config_uri: Union[str] = None
    customer_command: Union[str] = None       # 客户指令
    keyword: Union[str] = None                # 关键词
    customer_location: Union[str] = None      # 顾客位置
    product_uri: Union[str] = None            # 商品的图片地址
    virtual_human_word: Union[str] = None     # 虚拟人台词
    virtual_human_action: Union[str] = None   # 虚拟人动作

    class Config:
        schema_extra = {
            "example": {
                "store_id": faker.pyint(1, 10),
                "creator_id": faker.pyint(1, 100),
                "config_uri": "",
                "customer_command": "",
                "keyword": "",
                "customer_location": "",
                "product_uri": "",
                "virtual_human_word": "",
                "virtual_human_action": ""
            }}


class BlueprintUpdate(BaseModel):
    config_uri: Union[str] = None

    class Config:
        schema_extra = {
            "example": {
                "config_uri": "",
                "customer_command": "",
                "keyword": "",
                "customer_location": "",
                "product_uri": "",
                "virtual_human_word": "",
                "virtual_human_action": ""
            }}


class Blueprint(BaseModel):
    id: int
    store_id: int
    creator_id: int
    config_uri: str
    create_time: int
    update_time: int

    class Config:
        orm_mode = True
