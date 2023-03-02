# 元宇宙商户端文档 

### 服务简介
本服务是元宇宙电商平台商家端web后端服务，采用的python web框架:fastapi,
MVC架构，数据库模型用sqlalchemy1.4.9建立。

关于fastapi: https://fastapi.tiangolo.com/

## 后端服务器
### 域名与端口

测试线: http://frps.retailwell.com:20068/

生产线: http://frps.retailwell.com:20071/

注: 该域名通过frp注册，测试线的域名端口配置在dockefile里注明。生产线的域名端口在
helm的chart: deployment: meta-product-web-frpc 统一分配每个后端的frpc域名端口。

### 服务镜像
测试线: SXKJ:32775/meta_be
dockerfile: meta_be/Dockerfile

生产线: SXKJ:32775/meta_be_product
dockerfile: meta_be/Dockerfile_product

### 关于部署
测试线命名空间: pixel

生产线命名空间: meta-product

部署方式: 生产线采用helm本地仓库安装到k8s的方式部署

helm本地仓库地址：192.168.199.109服务器 /home/sxkj/wjh/my_resp/helm/meta-product-web/

### 查看日志
supervisorctl tail -f be

### 代码分支
测试线: master

生产线: product

## 数据库设计

### order

| 名称                | 类型           | 备注        |
|-------------------|--------------|-----------|
| back_reason       | VARCHAR(400) | 退款原因      |
| business_id       | INTEGER      | 商家ID      |
| close_time        | INTEGER      | 结束时间      |
| create_time       | INTEGER      | 创建时间      |
| customer_id       | INTEGER      | 买家ID      |
| deliver_address   | VARCHAR(150) | 发货地址      |
| deliver_time      | INTEGER      | 发货时间      |
| after_care_id     | INTEGER      | 退货id      |
| id                | INTEGER      | id        |
| logistic_id       | INTEGER      | 物流商id     |
| logistic_name     | VARCHAR(15)  | 物流商名称     |
| logistic_order_id | VARCHAR(30)  | 物流商快递物流ID |
| pay_count         | FLOAT        | 支付金额      |
| receiver_address  | VARCHAR(300) | 收货地址      |
| receiver_name     | VARCHAR(30)  | 收货人姓名     |
| receiver_phone    | VARCHAR(12)  | 收货电话      |
| recv_time         | INTEGER      | 收货时间      |
| status            | INTEGER      | 订单状态      |
| order_number      |VARCHAR(30)    |订单号        |
| sku_snapshot      |VARCHAR(1000)    |商品名称       |
| sku_id            |INTEGER        |库存ID       |
| num               |INTEGER        |购买数量|

### product
| 名称          | 类型           | 备注   |
|-------------|--------------|------|
| business_id | INTEGER      | 商家id |
| create_time | INTEGER      | 创建时间 |
| desc        | VARCHAR(150) | 商品描述 |
| id          | INTEGER      | id   |
| last_update | INTEGER      | 更新时间 |
| meta_obj_id | INTEGER      | 模型id |
| name        | VARCHAR(50)  | 名称   |
| unit        | VARCHAR(5)   | 单位名称 |

### except_order
| 名称                 | 类型           | 备注     |
|--------------------|--------------|--------|
| back_reason        | VARCHAR(400) | 退款原因   |
| business_id        | INTEGER      | 卖家id   |
| close_time         | INTEGER      | 关闭时间   |
| create_time        | INTEGER      | 下单时间   |
| deliver_time       | INTEGER      | 退货时间   |
| except_type        | VARCHAR(30)  | 异常类型   |
| id                 | INTEGER      | id     |
| logistics_id       | INTEGER      | 物流商家ID |
| logistics_order_id | INTEGER      | 物流号    |
| order_id           | INTEGER      | 订单ID   |
| recv_time          | INTEGER      | 收货时间   |
| remark             | VARCHAR(400) | 退款原因   |
| status             | INTEGER      | 服务状态   |
| back_cost             | FLOAT      | 退款金额   |

### sku
| 名称         | 类型           | 备注    |
|------------|--------------|-------|
| id         | INTEGER      | id    |
| price      | FLOAT        | 单价    |
| product_id | INTEGER      | 货物id  |
| sku_attr   | VARCHAR(200) | sku属性 |
| sku_name   | VARCHAR(100) | sku名称 |
| status     | INTEGER      | 状态    |
| stock      | INTEGER      | 库存量   |

### admin
| 名称            | 类型           | 备注       |
|---------------|--------------|----------|
| auth_token    | VARCHAR(255) | 登录token  |
| create_time   | INTEGER      | 创建时间     |
| id            | INTEGER      | id       |
| last_login    | INTEGER      | 最近时间     |
| password_hash | VARCHAR(255) | 加密后的登录密码 |
| update_time   | INTEGER      | 更新时间     |
| name      | VARCHAR(255) | 用户名      |

### customer
| 名称            | 类型           | 备注       |
|---------------|--------------|----------|
| auth_token    | VARCHAR(255) | 登录token  |
| create_time   | INTEGER      | 创建时间     |
| email_address | VARCHAR(255) | 邮箱地址     |
| id            | INTEGER      | id       |
| last_login    | INTEGER      | 最近时间     |
| password_hash | VARCHAR(255) | 加密后的登录密码 |
| tel_phone     | VARCHAR(11)  | 11位手机号   |
| update_time   | INTEGER      | 更新时间     |
| name      | VARCHAR(255) | 用户名      |

### scene
| 名称          | 类型           | 备注                     |
|-------------|--------------|------------------------|
| base_id     | INTEGER      | 基础场景id 1:博物馆 2:教室 3:家具 |
| config      | VARCHAR(255) | 配置文件                   |
| create_time | INTEGER      | 创建时间                   |
| creator     | VARCHAR(255) | 创建者                    |
| id          | INTEGER      | id                     |
| name        | VARCHAR(255) | 场景名称                   |
| tag         | INTEGER      | 场景标签 1:直播 2:商铺         |
| thumbnail   | VARCHAR(255) | 缩略图                    |

### scenebase
| 名称        | 类型           | 备注     |
|-----------|--------------|--------|
| id        | INTEGER      | id     |
| name      | VARCHAR(255) | 模版场景名称 |
| thumbnail | VARCHAR(255) | 缩略图    |

### user
| 名称            | 类型           | 备注           |
|---------------|--------------|--------------|
| auth_token    | VARCHAR(255) | 登录token      |
| create_time   | INTEGER      | 创建时间         |
| id            | INTEGER      | id           |
| last_login    | INTEGER      | 最近时间         |
| password_hash | VARCHAR(255) | 加密后的登录密码     |
| status        | INTEGER      | 状态 0:正常 1:禁用 |
| storename     | VARCHAR(50)  | 店铺名称         |
| update_time   | INTEGER      | 更新时间         |
| name      | VARCHAR(255) | 用户名          |

## 数据库配置
| key     | value         |
|---------|---------------|
| host    | 47.114.107.70 |
| port    | 5432          |
| user    | dbatest       |
| pwd     | sxwldba       | 
| db_name | dbatest       |

## 状态定义
| 作用域 | 状态  | 定义          |
|-----|-----|-------------|
| 订单  | 0   | 待发货         |
| 订单  | 1   | 待收货         |
| 订单  | 2   | 已完成         |
| 订单  | 3   | 已完成(退货退款)   |
| 订单  | 4   | 已完成(拒绝退货退款) |
| 订单  | -1  | 退款中         |
| 服务单 | 0   | 退款中         | 
| 服务单 | 1   | 商家同意        | 
| 服务单 | 2   | 商家拒绝        |
| sku | 0   | 缺货          | 
| sku | 1   | 有货          | 

