from sqlalchemy import Column, Integer, String
from app.models.database import BaseModel


class MarketingComponent(BaseModel):
    __tablename__ = 'marketing_component'

    id = Column(Integer, primary_key=True, index=True, comment='id')
    type = Column(String(50), comment='类型')
    content = Column(String(255), comment='内容')
    create_time = Column(Integer, comment='创建时间')
    update_time = Column(Integer, comment='更新时间')
