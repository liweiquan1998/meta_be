from sqlalchemy import Column, Integer, String, JSON
from app.models.database import BaseModel


class TTS(BaseModel):
    __tablename__ = "tts"
    id = Column(Integer, primary_key=True, index=True, comment='id')
    text_content = Column(String(255), comment='文本内容')
    text_id = Column(Integer, index=True, comment='文本id', nullable=False)
    sex = Column(Integer, comment='语音性别')
    status = Column(Integer, comment='状态')
    config_uri = Column(String(255), comment='音频文件地址')
    create_time = Column(Integer, comment='创建时间')
    update_time = Column(Integer, comment='更新时间')