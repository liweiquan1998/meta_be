from sqlalchemy import Column, Integer, String, JSON
from app.models.database import BaseModel


class Relation(BaseModel):
    __tablename__ = "relation"
    id = Column(Integer, primary_key=True, index=True, comment='id')
    relation_type = Column(String(255), comment='被使用类型')
    usage_scenario = Column(String(255), comment='场景')
    subject_id = Column(Integer, comment='使用者id')
    entity_id = Column(Integer, comment='被使用者id')
