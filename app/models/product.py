# @Time  : 2022-11-16 10:43
# @Author  : WanJinHong
# @File  : product.py
# @Email  : w1145253034@163.com
from sqlalchemy import Column, Integer, String,VARCHAR,TEXT
from app.models.database import BaseModel,Base

class Product(BaseModel):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, comment='id',autoincrement=True)
    business_id = Column(Integer,comment='商家id')
    create_time = Column(Integer,comment='创建时间')  # 加密后的登录密码
    last_update = Column(Integer,comment='更新时间')
    name = Column(VARCHAR(50),comment='名称')
    meta_obj_id = Column(Integer,comment='模型id')
    desc = Column(VARCHAR(150),comment='商品描述')
    unit = Column(VARCHAR(5),comment='单位名称')
    remarks = Column(TEXT,comment='备注')

if __name__ == '__main__':
    Base.metadata.create_all()



