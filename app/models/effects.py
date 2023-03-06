from sqlalchemy import Column, Integer, String

from app.models.database import BaseModel


class Effects(BaseModel):
    __tablename__ = "effects"
    id = Column(Integer, primary_key=True, index=True, comment='id')
    name = Column(String(255), comment='名称')
    pkg = Column(String(255), comment='pkg文件地址')
    thumbnail = Column(String(255), comment='缩略图地址')
    create_time = Column(Integer, comment='创建时间')
    create_id = Column(String(255), comment='创建者id')
    status = Column(Integer, comment='逻辑删除：0 正常,1 删除')
