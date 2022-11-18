# 元宇宙 DEMO

## 后端服务器
旧 http://frps.retailwell.com:20055/

新 http://frps.retailwell.com:20065/


## 查看日志
supervisorctl tail -f be

## 数据库设计

### order

| 名称   | 类型  | 备注  |
|------|-----|-----|
|back_reason|VARCHAR(400)|退款原因|
|business_id|INTEGER|商家ID|
|close_time|INTEGER|结束时间|
|create_time|INTEGER|创建时间|
|customer_id|INTEGER|买家ID|
|deliver_address|VARCHAR(150)|发货地址|
|deliver_time|INTEGER|发货时间|
|except_id|INTEGER|退货id|
|id|INTEGER|id|
|logistic_id|INTEGER|物流商id|
|logistic_name|VARCHAR(15)|物流商名称|
|logistic_order_id|VARCHAR(30)|物流商快递物流ID|
|pay_count|FLOAT|支付金额|
|receiver_address|VARCHAR(300)|收货地址|
|receiver_name|VARCHAR(30)|收货人姓名|
|receiver_phone|VARCHAR(12)|收货电话|
|recv_time|INTEGER|收货时间|
|status|INTEGER|订单状态|

### product
| 名称   | 类型  | 备注  |
|------|-----|-----|
|business_id|INTEGER|商家id|
|create_time|INTEGER|创建时间|
|desc|VARCHAR(150)|商品描述|
|id|INTEGER|id|
|last_update|INTEGER|更新时间|
|meta_obj_id|INTEGER|模型id|
|name|VARCHAR(50)|名称|
|unit|VARCHAR(5)|单位名称|

### except_order
| 名称   | 类型  | 备注  |
|------|-----|-----|
|back_reason|VARCHAR(400)|退款原因|
|business_id|INTEGER|卖家id|
|close_time|INTEGER|关闭时间|
|create_time|INTEGER|下单时间|
|deliver_time|INTEGER|退货时间|
|except_type|VARCHAR(30)|异常类型|
|id|INTEGER|id|
|logistics_id|INTEGER|物流商家ID|
|logistics_order_id|INTEGER|物流号|
|order_id|INTEGER|订单ID|
|recv_time|INTEGER|收货时间|
|remark|VARCHAR(400)|退款原因|
|status|INTEGER|服务状态|

###sku
| 名称   | 类型  | 备注  |
|------|-----|-----|
|id|INTEGER|id|
|price|FLOAT|单价|
|product_id|INTEGER|货物id|
|sku_attr|VARCHAR(200)|sku属性|
|sku_name|VARCHAR(100)|sku名称|
|status|INTEGER|状态|
|stock|INTEGER|库存量|

### admin
| 名称   | 类型  | 备注  |
|------|-----|-----|
|auth_token|VARCHAR(255)|登录token|
|create_time|INTEGER|创建时间|
|id|INTEGER|id|
|last_login|INTEGER|最近时间|
|password_hash|VARCHAR(255)|加密后的登录密码|
|update_time|INTEGER|更新时间|
|username|VARCHAR(255)|用户名|

### customer
| 名称   | 类型  | 备注  |
|------|-----|-----|
|auth_token|VARCHAR(255)|登录token|
|create_time|INTEGER|创建时间|
|email_address|VARCHAR(255)|邮箱地址|
|id|INTEGER|id|
|last_login|INTEGER|最近时间|
|password_hash|VARCHAR(255)|加密后的登录密码|
|tel_phone|VARCHAR(11)|11位手机号|
|update_time|INTEGER|更新时间|
|username|VARCHAR(255)|用户名|

### scene
| 名称   | 类型  | 备注  |
|------|-----|-----|
|base_id|INTEGER|基础场景id 1:博物馆 2:教室 3:家具|
|config|VARCHAR(255)|配置文件|
|create_time|INTEGER|创建时间|
|creator|VARCHAR(255)|创建者|
|id|INTEGER|id|
|name|VARCHAR(255)|场景名称|
|tag|INTEGER|场景标签 1:直播 2:商铺|
|thumbnail|VARCHAR(255)|缩略图|

### scenebase
| 名称   | 类型  | 备注  |
|------|-----|-----|
|id|INTEGER|id|
|name|VARCHAR(255)|模版场景名称|
|thumbnail|VARCHAR(255)|缩略图|

### user
| 名称   | 类型  | 备注  |
|------|-----|-----|
|auth_token|VARCHAR(255)|登录token|
|create_time|INTEGER|创建时间|
|id|INTEGER|id|
|last_login|INTEGER|最近时间|
|password_hash|VARCHAR(255)|加密后的登录密码|
|status|INTEGER|状态 0:正常 1:禁用|
|storename|VARCHAR(50)|店铺名称|
|update_time|INTEGER|更新时间|
|username|VARCHAR(255)|用户名|