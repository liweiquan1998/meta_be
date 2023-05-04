from pydantic import BaseModel
from faker import Faker
from typing import Optional, List
from fastapi_pagination import Params

faker = Faker(locale='zh_CN')

class SkuAttr(BaseModel):
    attribute_name: Optional[str]
    item: list
    selected: Optional[str]
class ProductSkuBase(BaseModel):
    sku_name: str
    sku_attr: List[SkuAttr]
    price: float
    stock: int
    unit: str = "件"
    business_id: int
    meta_obj_id: int
    remarks: str = ""


class ProductSkuUpdate(ProductSkuBase):
    sku_name: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    unit: Optional[str] = None
    business_id: Optional[int] = None
    meta_obj_id: Optional[int] = None
    remarks: Optional[str] = None
    status: Optional[int] = None


class ProductSkuParams(Params):
    name: Optional[str] = None
    status: Optional[int] = None
    create_time: Optional[int] = None


class ProductSkuParamsBase(BaseModel):
    name: Optional[str] = None
    status: Optional[int] = None
    create_time: Optional[int] = None


class ProductSkuCreate(ProductSkuBase):
    class Config:
        schema_extra = {
            "example": {
                "sku_name": faker.pystr(),
                "sku_attr": [],
                "price": faker.pyint(5, 2000),
                "stock": faker.pyint(1, 100),
                "unit": "件",
                "remarks": faker.pystr(),
                "business_id": faker.pyint(1, 100),
                "meta_obj_id": faker.pyint(1, 100)
            }}


class Sku(ProductSkuBase):
    desc: str
    sku_attr: List[SkuAttr]

    class Config:
        orm_mode = True
