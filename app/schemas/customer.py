from typing import Union

from pydantic import BaseModel
from faker import Faker

faker = Faker(locale='zh_CN')


class CustomerBase(BaseModel):
    tel_phone: str
    email_address: str

class CustomerCreate(CustomerBase):
    username: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "username": faker.name(),
                "password": faker.password(),
                "tel_phone": faker.phone_number(),
                "email_address": faker.email()}}

class CustomerGet(BaseModel):
    username: Union[str, None] = None
    last_login: Union[int, None] = None


class Customer(CustomerBase):
    id: int
    username: str
    create_time: int
    update_time: int
    last_login: int

    class Config:
        orm_mode = True
