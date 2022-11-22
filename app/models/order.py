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
    sku_list = Column(JSON,comment='sku和对应的数量')  # 加密后的登录密码
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

    @classmethod
    def get_status_define(cls):
        return {
            0: "待付款", 1:"待发货", 2: "已发货", 3: "已完成", 4: "已关闭",
            -1: "申请退货", -2: "同意退货", -3:"退货成功",-4: "退款成功"
        }



if __name__ == '__main__':
    Base.metadata.create_all()



