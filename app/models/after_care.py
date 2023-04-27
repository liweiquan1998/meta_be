# @Time  : 2022-11-16 10:43
# @Author  : WanJinHong
# @File  : product.py
# @Email  : w1145253034@163.com
from sqlalchemy import Column, Integer, String,VARCHAR,Float,JSON
from app.models.database import BaseModel,Base

class AfterCare(BaseModel):
    __tablename__ = "after_care"
    id = Column(Integer, primary_key=True, comment='id',autoincrement=True)
    except_type = Column(VARCHAR(30),comment='异常类型',default='退货退款')
    status = Column(Integer,comment='服务状态',default=0)
    create_time = Column(Integer,comment='下单时间')
    deliver_time = Column(Integer,comment='退货时间')
    recv_time = Column(Integer,comment='收货时间')
    close_time = Column(Integer,comment='关闭时间')
    order_id = Column(Integer,comment='订单ID')
    logistics_order_id = Column(Integer,comment='物流号')
    logistics_id = Column(Integer,comment='物流商家ID')
    business_id = Column(Integer,comment='卖家id',index=True)
    back_reason = Column(VARCHAR(400),comment='退款原因')
    remark = Column(VARCHAR(400),comment='退款备注')
    back_cost = Column(Float,comment='退款金额')

    @classmethod
    def get_status_define(cls):
        return {
            1: "等待商家确认", 2: "商家同意", 3: "等待商家确认收货", 4: "售后完成"
        }



if __name__ == '__main__':
    Base.metadata.create_all()



