from sqlalchemy import Column, Integer, String

from app.models.database import BaseModel


class VirtualHuman(BaseModel):
    __tablename__ = 'virtual_human'

    id = Column(Integer, primary_key=True, index=True, comment='id')
    name = Column(String(20), comment='姓名')
    sex = Column(Integer, comment='性别 1:男 2:女')
    status = Column(Integer, comment='状态 0:禁用 1:启用')
    creator_id = Column(Integer, comment='创建者id')
    create_time = Column(Integer, comment='创建时间')
    headimg_uri = Column(String(50), comment='头像地址')
    work_space = Column(String(50), comment='命名空间')
