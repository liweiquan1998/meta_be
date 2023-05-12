from sqlalchemy import Column, Integer, String, JSON
from app.models.database import BaseModel


class BluePrint(BaseModel):
    __tablename__ = "blueprint"
    id = Column(Integer, primary_key=True, index=True, comment='id')
    store_id = Column(Integer, index=True, comment='店铺ID', nullable=False)
    creator_id = Column(Integer, comment='创建人id')
    create_time = Column(Integer, comment='创建时间')
    update_time = Column(Integer, comment='更新时间')
    graphdata = Column(JSON, comment='图数据')
    nodedata = Column(JSON, comment='节点数据')
    uedata = Column(JSON, comment='ue数据')

