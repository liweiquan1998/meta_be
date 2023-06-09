from pydantic import BaseModel
from faker import Faker

faker = Faker(locale='zh_CN')


class AdminBase(BaseModel):
    tel_phone: str
    email_address: str


class AdminCreate(BaseModel):
    name: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "name": faker.name(),
                "password": faker.password()}}

class AdminLogin(BaseModel):
    name: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "name": faker.name(),
                "password": faker.password()}}


class AdminUpdate(AdminBase):
    password_hash: str


class Admin(AdminBase):
    id: int
    name: str
    password_hash: str
    auth_token: str
    create_time: int
    update_time: int
    last_login: int

    class Config:
        orm_mode = True
