# @Time  : 2022-11-16 10:43
# @Author  : WanJinHong
# @File  : product.py
# @Email  : w1145253034@163.com
from sqlalchemy import Column, Integer, String, VARCHAR, Float
from app.models.database import BaseModel, Base


class Sku(BaseModel):
    __tablename__ = "sku"
    id = Column(Integer, primary_key=True, comment='id', autoincrement=True)
    product_id = Column(Integer, comment='货物id')
    sku_attr = Column(VARCHAR(200), comment='sku属性')  # 加密后的登录密码
    sku_name = Column(VARCHAR(100), comment='sku名称')
    price = Column(Float, comment='单价')
    status = Column(Integer, comment='状态')
    stock = Column(Integer, comment='库存量')

    @classmethod
    def get_status_define(cls):
        return {1: {"status": "有货"}, 0: {"status": "缺货"}}


if __name__ == '__main__':
    Base.metadata.create_all()
