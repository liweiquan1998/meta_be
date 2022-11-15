from sqlalchemy import Column, Integer, String

from app.models.database import BaseModel



class Customer(BaseModel):
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255))
    password_hash = Column(String(255))  # 加密后的登录密码
    auth_token = Column(String(255))  # 登录token
    tel_phone = Column(String(11))  # 11位手机
    email_address = Column(String(255))
    create_time = Column(Integer)  # 创建时间
    update_time = Column(Integer)  # 更新时间
    last_login = Column(Integer)  # 最近时间


