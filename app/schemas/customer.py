from pydantic import BaseModel
from faker import Faker
faker = Faker(locale='zh_CN')

class CustomerBase(BaseModel):
    tel_phone: str
    email_address: str


class CustomerCreate(CustomerBase):
    password_hash: str
    username: str
    auth_token: str

    class Config:
        schema_extra = {
            "example": {
                "username": faker.name(),
                "password_hash": faker.password(),
                "auth_token": faker.password(),
                "tel_phone": faker.phone_number(),
                "email_address": faker.email()}}


class CustomerUpdate(CustomerBase):
    password_hash: str


class Customer(CustomerBase):
    id: int
    username: str
    password_hash: str
    auth_token: str
    create_time: int
    update_time: int
    last_login: int

    class Config:
        orm_mode = True


