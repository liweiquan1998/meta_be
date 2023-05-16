from sqlalchemy import Column, Integer, String, JSON
from app.models.database import BaseModel


class TTS(BaseModel):
    __tablename__ = "tts"
    id = Column(Integer, primary_key=True, index=True, comment='id')
    text_id = Column(Integer, index=True, comment='店铺ID', nullable=False)
    sex = Column(Integer, comment='创建人id')
    status = Column(Integer, comment='状态')
    config_uri = Column(String(255), comment='音频文件地址')
    create_time = Column(Integer, comment='创建时间')
    update_time = Column(Integer, comment='更新时间')