from sqlalchemy import Column, Integer, String, Float

from app.models.database import BaseModel


class MetaObj(BaseModel):
    __tablename__ = "meta_obj"
    id = Column(Integer, primary_key=True, index=True, comment='id')
    name = Column(String(255), comment='名称')
    type = Column(Integer, comment='类型 0: upload 1: image 2: video')
    kind = Column(Integer, comment='种类 0:场景素材 1:商品')  # todo  改为category

    aigc = Column(String(999999), comment='aigc源地址')
    status = Column(Integer, comment='商品状态 0:渲染中 1:已完成 2:渲染失败')

    model = Column(String(255), comment='模型文件地址')
    thumbnail = Column(String(255), comment='缩略图地址')
    media = Column(String(255), comment='视频地址')
    tag = Column(String(255), comment='物品种类')  # todo  字段名改为tags  json格式，存多个tag

    create_time = Column(Integer, comment='创建时间')
    creator_id = Column(Integer, comment='创建者id')
    height = Column(Float, comment='物品高度')
    ue_address = Column(String(255), comment='ue地址')
