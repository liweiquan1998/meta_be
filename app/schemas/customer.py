from pydantic import BaseModel


class CustomerBase(BaseModel):
    tel_phone: str
    email_address: str


class CustomerCreate(CustomerBase):
    password_hash: str
    username: str


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
