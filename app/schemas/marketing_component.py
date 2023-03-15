from typing import Optional

from pydantic import BaseModel


class MarketingComponentCreate(BaseModel):
    type: str
    content: str

    class Config:
        schema_extra = {
            "example": {
                "type": "customer_command",
                "content": '你好',
            }}


class MarketingComponentUpdate(BaseModel):
    content: str

    class Config:
        schema_extra = {
            "example": {
                "content": '你好xxxx',
            }}


class MarketingComponentGet(BaseModel):
    type: str

