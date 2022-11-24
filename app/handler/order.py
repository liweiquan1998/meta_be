# @Time  : 2022-11-17 14:14
# @Author  : WanJinHong
# @File  : order.py
# @Email  : w1145253034@163.com
from app.crud.order import *
from app.crud.except_order import *
from app.crud.sku import *
from app.models import Order,Sku
import time

status_define = Order.get_status_define()

def deliver_order(db: Session, item_id: int,item:schemas.OrderDeliver):
    order = get_order_once(db,item_id)
    if not order:
        raise Exception(404,'未找到该任务')
    if order.status == 0:
        if deliver_check(order):
            for k,v in item.dict(exclude_unset=True).items():
                setattr(order, k, v)
            order.status = 1
            order.deliver_time = time.time()
            sku_id = order.sku_id
            sku = get_sku_once(db,sku_id)
            if sku.stock < order.num:
                raise Exception(405,f'发货失败，{sku.sku_name}库存不足')
            else:
                sku.stock -= order.num
            db.commit()
            db.refresh(order)
            return order
        else:
            raise Exception(400,f'选择发货的订单状态为:{status_define.get(order.status)}')
    else:
        raise Exception(400,f'选择发货的订单状态为:{status_define.get(order.status)}')


def deliver_check(order:Order):
    return True


def except_order(db: Session, item_id: int,item:schemas.OrderExcept):
    order_db_item = get_order_once(db,item_id)
    if not order_db_item:
        raise Exception(404,'未找到该任务')
    if order_db_item.status == -1:  # 服务中
        except_order_db_item = get_except_order_once(db,order_db_item.except_id)
        if not except_order_db_item:
            raise Exception(404,'未找到服务号')
        except_order_db_item.set_field(item.dict())
        except_order_db_item.status = 1
        order_db_item.status = item.status  # 已完成(退货退款)
        order_db_item.close_time = time.time()
        sku_db_item = get_sku_once(db,order_db_item.sku_id)
        num = order_db_item.num
        sku_db_item.stock += num
        db.commit()
        db.flush()
        res:dict = except_order_db_item.to_dict()
        res.update(order_db_item.to_dict())
        return res
    else:
        raise Exception('该订单不是服务中状态，不可退货退款')

