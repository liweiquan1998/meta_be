from sqlalchemy import Column, Integer, String

from app.models.database import BaseModel


class SceneBase(BaseModel):
    __tablename__ = "scene_base"
    id = Column(Integer, primary_key=True, index=True, comment='id')
    name = Column(String(255), comment='模版场景名称')
    thumbnail = Column(String(255), comment='缩略图')
