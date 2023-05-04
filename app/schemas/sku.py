from pydantic import BaseModel
from faker import Faker
faker = Faker(locale='zh_CN')


class SkuBase(BaseModel):
    product_id: int
    sku_attr: list
    sku_name: str
    price: float
    stock: int



class SkuCreate(SkuBase):

    class Config:
        schema_extra = {
            "example": {
                "product_id": faker.pyint(),
                "sku_attr": [],
                "sku_name": faker.pystr(),
                "price": faker.pyint(5,2000),
                "stock" : faker.pyint(1,100),
            }}


class SkuUpdate(SkuBase):
    pass


class Sku(SkuBase):
    pass

    class Config:
        orm_mode = True


