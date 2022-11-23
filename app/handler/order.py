# @Time  : 2022-11-17 14:14
# @Author  : WanJinHong
# @File  : order.py
# @Email  : w1145253034@163.com
from app.crud.order import *
from app.crud.sku import *
from app.models import Order,Sku
import time

status_define = Order.get_status_define()

def deliver_order(db: Session, item_id: int,item:schemas.OrderDeliver):
    order = get_order_once(db,item_id)
    if not order:
        raise Exception(404,'未找到该任务')
    if order.status == 1:
        if deliver_check(order):
            for k,v in item.dict(exclude_unset=True).items():
                setattr(order, k, v)
            order.status = 2
            order.deliver_time = time.time()
            sku_id = order.sku_id
            sku = get_sku_once(db,sku_id)
            if sku.stock < order.num:
                raise Exception(422,f'发货失败，{sku.sku_name}库存不足')
            else:
                sku.stock -= order.num
            db.commit()
            db.refresh(order)
            return order
        else:
            raise Exception(422,f'选择发货的订单状态为:{status_define.get(order.status)}')
    else:
        raise Exception(422,f'选择发货的订单状态为:{status_define.get(order.status)}')


def deliver_check(order:Order):
    return True