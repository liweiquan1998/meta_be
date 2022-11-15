from sqlalchemy import Column, Integer, String

from configs.database import BaseModel



class Customer(BaseModel):
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(128))
    password_hash = Column(String(128))  # 加密后的登录密码
    auth_token = Column(String(128))  # 登录token
    tel_phone = Column(String(11))  # 11位手机
    email_address = Column(String(128))
    create_time = Column(Integer)  # 创建时间
    update_time = Column(Integer)  # 更新时间
    last_login = Column(Integer)  # 最近时间


