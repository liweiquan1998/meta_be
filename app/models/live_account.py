from sqlalchemy import Column, Integer, String
from app.models.database import BaseModel


class LiveAccount(BaseModel):
    __tablename__ = "live_account"
    id = Column(Integer, primary_key=True, index=True, comment='id')
    name = Column(String(255), comment='直播账号名称')
    address = Column(String(255), comment='直播推流地址')
    platform = Column(String(255), comment='直播推流平台')
    key = Column(String(255), comment='串流密钥')
    token = Column(String(255), comment='串流token')
    creator_id = Column(Integer, comment='创建者id')
    last_time = Column(Integer, comment='首次创建直播的时间')
    status = Column(Integer)