from pydantic import BaseModel
from faker import Faker
faker = Faker(locale='zh_CN')


class ProductSkuBase(BaseModel):
    price: float
    stock: int
    desc: str
    unit: str
    business_id: int
    meta_obj_id: int
    remarks: str

class ProductSkuUpdate(ProductSkuBase):
    pass


class ProductSkuCreate(ProductSkuBase):
    class Config:
        schema_extra = {
            "example": {
                "price": faker.pyint(5,2000),
                "stock": faker.pyint(1,100),
                "desc": faker.pystr(),
                "unit": "件",
                "remarks": faker.pystr(),
                "business_id": faker.pyint(1,100),
                "meta_obj_id": faker.pyint(1,100)
            }}


class Sku(ProductSkuBase):
    pass

    class Config:
        orm_mode = True


