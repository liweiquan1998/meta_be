from sqlalchemy import Column, Integer, String

from app.models.database import BaseModel


class MarketingContent(BaseModel):
    __tablename__ = 'marketing_content_'

    id = Column(Integer, primary_key=True, index=True, comment='id')
    name = Column(String(20), comment='名称')
    content = Column(String(10000), comment='内容')
    metaobj_id = Column(Integer, comment='关联的metaobj_id')
    creator_id = Column(Integer, comment='创建者id')
    virtual_human_id = Column(Integer, comment='关联的虚拟人id')
    create_time = Column(Integer, comment='创建时间')
    status = Column(Integer, comment='状态 1、2:音频生成中、已生成  3、4:视频生成中、已生成')  # todo: 状态意义
    audio_uri = Column(String(50), comment='音频地址')
    video_uri = Column(String(50), comment='视频地址')
    work_space = Column(String(50), comment='命名空间')
