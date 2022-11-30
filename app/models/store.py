from sqlalchemy import Column, Integer, String
from app.models.database import BaseModel


class Store(BaseModel):
    __tablename__ = "store"
    id = Column(Integer, primary_key=True, index=True, comment='id')
    name = Column(String(255), comment='店铺名称')
    scene_id = Column(Integer, comment='场景id')
    thumbnail = Column(String(255), comment='缩略图')
    config = Column(String(255), comment='配置文件')
    creator_id = Column(String(255), comment='创建者id')
    create_time = Column(Integer, comment='创建时间')
    creator_name = Column(String(255), comment='创建者名称')
