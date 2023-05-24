from sqlalchemy import Column, Integer, String, JSON

from app.models.database import BaseModel

class Shelves(BaseModel):
    __tablename__ = "shelves"
    id = Column(Integer, primary_key=True, index=True, comment='id')
    scene_id = Column(Integer, comment='场景id')
    data = Column(JSON, comment='货架数据')
    shelf_id = Column(String(255), comment='货架id')