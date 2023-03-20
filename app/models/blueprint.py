from sqlalchemy import Column, Integer, String, JSON
from app.models.database import BaseModel


class BluePrint(BaseModel):
    __tablename__ = "blueprint"
    id = Column(Integer, primary_key=True, index=True, comment='id')
    store_id = Column(Integer, index=True, comment='店铺ID', nullable=False)
    creator_id = Column(Integer, comment='创建人id')
    config_uri = Column(String(100), comment='蓝图配置')
    customer_command = Column(String(255), comment='客户指令')
    keyword = Column(String(255), comment='关键词')
    customer_location = Column(String(255), comment='顾客位置')
    product_uri = Column(String(255), comment='商品图片地址')
    virtual_human_word = Column(String(255), comment='虚拟人台词')
    virtual_human_action = Column(String(255), comment='虚拟人动作')
    create_time = Column(Integer, comment='创建时间')
    update_time = Column(Integer, comment='更新时间')
