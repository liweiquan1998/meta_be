from pydantic import BaseModel
from faker import Faker

faker = Faker(locale='zh_CN')

class MetaObjTagPost(BaseModel):
    name: str

    class Config:
        schema_extra = {
            "example": {
                "name": '桌子'
            }}

