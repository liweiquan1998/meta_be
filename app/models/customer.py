from sqlalchemy import Column, Integer, String

from app.models.database import BaseModel


class Customer(BaseModel):
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True, index=True, comment='id')
    username = Column(String(255), comment='用户名')
    password_hash = Column(String(255), comment='加密后的登录密码')
    auth_token = Column(String(255), comment='登录token')
    headimg_uri = Column(String(255), comment='头像')
    tel_phone = Column(String(11), comment='11位手机号')
    email_address = Column(String(255), comment='邮箱地址')
    deliver_address = Column(String(255), comment='收获地址')
    sex = Column(Integer, comment='性别：1为男，2为女')
    create_time = Column(Integer, comment='创建时间')
    update_time = Column(Integer, comment='更新时间')
    last_login = Column(Integer, comment='最近时间')