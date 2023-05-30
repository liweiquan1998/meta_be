from sqlalchemy import Column, Integer, String

from app.models.database import BaseModel


# 场景表
class Scene(BaseModel):
    __tablename__ = "scene"
    id = Column(Integer, primary_key=True, index=True, comment='id')
    name = Column(String(50), comment='场景名称')
    thumbnail = Column(String(255), comment='缩略图')
    config_file = Column(String(255), comment='配置文件')
    tag = Column(Integer, comment='标签（0：all，1：元商店，2：直播）')
    stage = Column(Integer, comment='阶段（0：硬装，1：软装，2：应用）')
    base_id = Column(Integer, comment='基础场景id')
    store_id = Column(Integer, comment='商店id')
    create_id = Column(Integer, comment='创建者id')
    create_time = Column(Integer, comment='创建时间')
    update_id = Column(Integer, comment='更新者id')
    update_time = Column(Integer, comment='更新时间')
