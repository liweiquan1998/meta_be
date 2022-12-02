from sqlalchemy import Column, Integer, String

from app.models.database import BaseModel



class User(BaseModel):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True, comment='id')
    name = Column(String(255), comment='用户名', unique=True)
    storename = Column(String(50), comment='店铺名称')
    password_hash = Column(String(255), comment='加密后的登录密码')
    auth_token = Column(String(255), comment='登录token')
    create_time = Column(Integer, comment='创建时间')
    update_time = Column(Integer, comment='更新时间')
    last_login = Column(Integer, comment='最近时间')
    status = Column(Integer, comment='状态 0:正常 1:禁用')
    tel_phone = Column(String(255), comment='电话')



