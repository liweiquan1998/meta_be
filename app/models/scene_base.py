from sqlalchemy import Column, Integer, String

from app.models.database import BaseModel

class Scene_base(BaseModel):
    __tablename__ = "scene_base"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))  # base场景名称

