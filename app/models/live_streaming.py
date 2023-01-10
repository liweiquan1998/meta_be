from sqlalchemy import Column, Integer, String
from app.models.database import BaseModel


class LiveStreaming(BaseModel):
    __tablename__ = "live_streaming"
    id = Column(Integer, primary_key=True, index=True, comment='id')
    name = Column(String(255), comment='直播间名称')
    address = Column(String(255), comment='直播间地址')
    status = Column(Integer, comment='直播间状态 0:未开播 1:直播中')
    create_time = Column(Integer, comment='创建时间')
    virtual_human_id = Column(Integer, comment='虚拟人id')
    base_scene_id = Column(Integer, comment='基础场景id')
    creator_id = Column(Integer, comment='创建者id')
    live_account_id = Column(Integer, comment='直播账户id')
    config = Column(String(255), comment='配置文件的路径')

