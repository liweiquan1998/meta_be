from typing import Optional

from pydantic import BaseModel
from faker import Faker

faker = Faker(locale='zh_CN')


class AfterCareBase(BaseModel):
    except_type: Optional[str] = None
    order_id: int
    business_id: Optional[int] = None
    back_reason: Optional[str] = None


class AfterCareCreate(AfterCareBase):
    class Config:
        schema_extra = {
            "example": {
                "back_reason": "不想要了",
                "except_type": "退货退款",
                "order_id": faker.pyint(1, 10),
                "business_id": faker.pyint(1, 10)
            }}


class AfterCareUpdate(AfterCareBase):
    remark: Optional[str] = None
    status: int
    create_time: Optional[int] = None
    deliver_time: Optional[int] = None
    recv_time: Optional[int] = None
    close_time: Optional[int] = None

class BusinessAfterCareUpdate(BaseModel):
    remark: str
    status: int

class AfterCare(AfterCareBase):
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

