from pydantic import BaseModel
from faker import Faker
faker = Faker(locale='zh_CN')


class ProductBase(BaseModel):
    name: str
    meta_obj_id: int
    desc: str
    unit: str



class ProductCreate(ProductBase):
    business_id: int
    create_time: int

    class Config:
        schema_extra = {
            "example": {
                "business_id": faker.pyint(),
                "create_time": faker.unix_time(start_datetime="-7d",end_datetime="now"),
                "unit": "件",
                "name": faker.email(),
                "meta_obj_id": faker.pyint(),
                "desc" : faker.pystr()
            }}


class ProductUpdate(ProductBase):
    last_update: int


class Product(ProductBase):
    last_update: int
    create_time: int

    class Config:
        orm_mode = True


