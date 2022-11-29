from sqlalchemy import Column, Integer, String

from app.models.database import BaseModel


class Scene(BaseModel):
    __tablename__ = "scene"
    id = Column(Integer, primary_key=True, index=True, comment='id')
    name = Column(String(255), comment='场景名称')
    tag = Column(Integer, comment='场景标签 1:直播 2:商铺')
    base_id = Column(Integer, comment='基础场景id 1:博物馆 2:教室 3:家具')
    thumbnail = Column(String(255), comment='缩略图')
    config = Column(String(255), comment='配置文件')
    creator_id = Column(String(255), comment='创建者id')
    create_time = Column(Integer, comment='创建时间')
