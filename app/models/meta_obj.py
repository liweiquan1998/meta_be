from sqlalchemy import Column, Integer, String

from app.models.database import BaseModel

class MetaObj(BaseModel):
    __tablename__ = "meta_obj"
    id = Column(Integer, primary_key=True, index=True, comment='id')
    name = Column(String(255), comment='名称')
    type = Column(Integer, comment='类型 0: upload 1: aigc')
    aigc = Column(String(255), comment='aigc源地址')
    model = Column(String(255), comment='模型文件地址')
    thumbnail = Column(String(255), comment='缩略图地址')
