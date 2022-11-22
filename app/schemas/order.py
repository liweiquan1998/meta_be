from pydantic import BaseModel
from faker import Faker
from fastapi_pagination import Params

faker = Faker(locale='zh_CN')
import random as rd


class OrderBase(BaseModel):
    sku_list: str
    pay_count: float
    business_id: int
    customer_id: int
    receiver_phone: str
    deliver_address: str
    logistic_order_id: str
    receiver_address: str
    receiver_name: str
    postal_code: str

class OrderCreate(OrderBase):
    class Config:
        schema_extra = {
            "example": {
                "sku_list": '[{"sku_id":%s,"num":%s}]' % (faker.pyint(1, 5), faker.pyint(1, 5)),
                "pay_count": faker.pyint(1, 100),
                "business_id": faker.pyint(1, 100),
                "customer_id": faker.pyint(1, 100),
                "receiver_phone": faker.phone_number(),
                "deliver_address": faker.address(),
                "logistic_order_id": faker.pyint(1, 100),
                "receiver_address": faker.address(),
                "receiver_name": faker.name()
            }}


class OrderDeliver(BaseModel):
    logistic_id: int
    logistic_name: str
    logistic_order_id: str

    class Config:
        schema_extra = {
            "example": {
                "logistic_id": faker.pyint(1, 10),
                "logistic_name": rd.choice(['百世快递', '韵达快递', '圆通快递', '申通快递', '中通快递']),
                "logistic_order_id": str(faker.pyint(100000,200000))
            }}


class OrderUpdate(OrderBase):
    create_time: int
    deliver_time: int
    recv_time: int
    close_time: int
    except_id: int
    back_reason: str




class Order(OrderBase):
    logistic_id: int
    logistic_name: str
    create_time: int
    deliver_time: int
    recv_time: int
    close_time: int
    order_id: int
    back_reason: str

    class Config:
        orm_mode = True

class BusinessPageParams(Params):
    business_id: int

class CustomerPageParams(Params):
    customer_id: int