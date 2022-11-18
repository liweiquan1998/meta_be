
from pydantic import BaseModel
from faker import Faker

faker = Faker(locale='zh_CN')


class ExceptOrderBase(BaseModel):
    except_type: str
    order_id: int
    business_id: int
    back_reason: str


class ExceptOrderCreate(ExceptOrderBase):
    class Config:
        schema_extra = {
            "example": {
                "back_reason": "不想要了",
                "except_type": "退货退款",
                "order_id": faker.pyint(1, 10),
                "business_id": faker.pyint(1, 10)
            }}


class ExceptOrderUpdate(ExceptOrderBase):
    remark: str
    status: int
    create_time: int
    deliver_time: int
    recv_time: int
    close_time: int

class BusinessExceptOrderUpdate(BaseModel):
    remark: str
    status: int

class ExceptOrder(ExceptOrderBase):
    back_reason: str
    remark: str
    status: int
    create_time: int
    deliver_time: int
    recv_time: int
    close_time: int
    logistics_order_id: int

    class Config:
        orm_mode = True

