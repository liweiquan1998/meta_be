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
    occupied = Column(Integer, comment='0:可登陆，2:不可登陆(被其他浏览器占用)，None:可登陆')
    email_address = Column(String(40), comment='邮箱地址')
    last_ping = Column(Integer, comment='ws上次ping前端的时间')
    group_id = Column(Integer, comment='用户组ID')

