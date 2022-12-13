from sqlalchemy import Column, Integer, String

from app.models.database import BaseModel


class Background(BaseModel):
    __tablename__ = "background"
    id = Column(Integer, primary_key=True, index=True, comment='id')
    name = Column(String(255), comment='背景名称')
    type = Column(Integer, comment='背景类型 0:image 1:video')
    file_uri = Column(String(255), comment='文件地址')
    create_time = Column(Integer, comment='创建时间')
    creator_id = Column(Integer, comment='创建者id')