from sqlalchemy import Column, Integer, String

from app.models.database import BaseModel

class MetaObjTag(BaseModel):
    __tablename__ = "meta_obj_tag"
    id = Column(Integer, primary_key=True, index=True, comment='id')
    name = Column(String(255), comment='标签')
