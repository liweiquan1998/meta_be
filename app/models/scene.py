from sqlalchemy import Column, Integer, String

from app.models.database import BaseModel


class Scene(BaseModel):
    __tablename__ = "scene"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))  # 场景名称
    tag = Column(Integer)  # 场景标签 1:直播 2:商铺
    base_id = Column(Integer)  # 基础场景id
    thumbnail = Column(String(255))  # 缩略图
    config = Column(String(255))  # 配置文件
    creator = Column(String(255))  # 创建者
    create_time = Column(Integer)  # 创建时间
