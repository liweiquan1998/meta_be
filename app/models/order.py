# @Time  : 2022-11-16 10:43
# @Author  : WanJinHong
# @File  : product.py
# @Email  : w1145253034@163.com
from sqlalchemy import Column, Integer, String,VARCHAR,Float,JSON
from app.models.database import BaseModel,Base

class Order(BaseModel):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True, comment='id',autoincrement=True)
    status = Column(Integer,comment='订单状态')
    create_time = Column(Integer,comment='创建时间')
    deliver_time = Column(Integer,comment='发货时间')
    recv_time = Column(Integer,comment='收货时间')
    close_time = Column(Integer,comment='结束时间')
    pay_count = Column(Float,comment='支付金额')
    except_id = Column(Integer,comment='退货id')
    business_id = Column(Integer,comment='商家ID',index=True)
    customer_id = Column(Integer,comment='买家ID')
    receiver_phone = Column(String(12),comment='收货电话')
    deliver_address = Column(VARCHAR(150),comment='发货地址')
    logistic_id = Column(Integer,comment='物流商id')
    logistic_name = Column(VARCHAR(15),comment='物流商名称')
    back_reason = Column(VARCHAR(400),comment='退款原因')
    logistic_order_id = Column(VARCHAR(30),comment='物流商快递物流ID')
    receiver_address = Column(VARCHAR(300),comment='收货地址')
    receiver_name = Column(VARCHAR(30),comment='收货人姓名')
    postal_code = Column(VARCHAR(10),comment='邮编')

    order_number = Column(VARCHAR(30),comment='订单编号')
    sku_id = Column(Integer,comment='库存id')
    num = Column(Integer,comment='购买数量')
    sku_snapshot = Column(VARCHAR(500),comment='sku快照')

    @classmethod
    def get_status_define(cls):
        return {
            0: "待发货", 1:"待收货", 2: "已完成",3: "已完成(同意退货退款)",4: "已完成(拒绝退货退款)",
            -1: "售后中"
        }


if __name__ == '__main__':
    Base.metadata.create_all()



