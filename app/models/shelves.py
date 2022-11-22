from sqlalchemy import Column, Integer, String

from app.models.database import BaseModel

class Shelves(BaseModel):
    __tablename__ = "shelves"
    id = Column(Integer, primary_key=True, index=True, comment='id')
    scene_id = Column(Integer, comment='场景id')
    config = Column(String(255), comment='配置文件')
