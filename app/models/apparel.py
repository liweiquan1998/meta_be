from sqlalchemy import Column, Integer, String,VARCHAR,Float,JSON
from app.models.database import BaseModel,Base


class Apparel(BaseModel):
    __tablename__ = 'apparel'

    id = Column(Integer, primary_key=True)
    work_space = Column(String(50))
    apparel_name = Column(String(50))
    apparel_type = Column(Integer)
    thumbnail = Column(String(255))
    file_uri = Column(String(255))

