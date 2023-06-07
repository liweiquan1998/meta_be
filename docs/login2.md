# 登录模块

- /create
- /login
- /swagger/login

一）：/create

- 创建商户

![image-20230605173610022](C:\Users\86178\AppData\Roaming\Typora\typora-user-images\image-20230605173610022.png)



1. 用户通过前端发送数据，后端接收到数据后，会去数据库中查询，并进行判断，如果不存在相同的用户名和店铺名时，表示校验成功，可以创建

2. 如若发现数据已经存在，那么抛出异常进行处理

   

###### 示例：

- 请求体：

![image-20230605191109752](C:\Users\86178\AppData\Roaming\Typora\typora-user-images\image-20230605191109752.png)

- 成功

![image-20230605190610302](C:\Users\86178\AppData\Roaming\Typora\typora-user-images\image-20230605190610302.png)

- 失败

![image-20230605191154046](C:\Users\86178\AppData\Roaming\Typora\typora-user-images\image-20230605191154046.png)





二）：/login【登录】

- 商户登录

![image-20230605182046025](C:\Users\86178\AppData\Roaming\Typora\typora-user-images\image-20230605182046025.png)



1. 用户通过前端发送登录请求
2. 后端查询数据库，判断用户数据是否正确
3. 正确：判断该用户是否被占用
   - 被占用：无法登录
   - 未占用：允许登录
4. 错误：数据校验失败，返回响应信息



###### 示例：

- 请求体

![image-20230605190646366](C:\Users\86178\AppData\Roaming\Typora\typora-user-images\image-20230605190646366.png)



- 成功：

![image-20230605190710982](C:\Users\86178\AppData\Roaming\Typora\typora-user-images\image-20230605190710982.png)

- 失败

Response

![image-20230605190753523](C:\Users\86178\AppData\Roaming\Typora\typora-user-images\image-20230605190753523.png)





三）：/swagger/login【token登录】

- 携带token的登录

![image-20230605183444653](C:\Users\86178\AppData\Roaming\Typora\typora-user-images\image-20230605183444653.png)

1. 首先，用户发送登录请求时，前端会携带一个token值，这个值会被送给后端，后端进行验证
2. 验证成功
   - 后端查询数据库，判断用户数据是否正确
   - 正确：判断该用户是否被占用
     - 被占用：无法登录
     - 未占用：允许登录
   - 错误：数据校验失败，返回响应信息
3. 验证失败
   - 抛出异常



###### 示例：

- 请求体

![image-20230605191330810](C:\Users\86178\AppData\Roaming\Typora\typora-user-images\image-20230605191330810.png)

- 成功

![image-20230605191437495](C:\Users\86178\AppData\Roaming\Typora\typora-user-images\image-20230605191437495.png)

- 失败

![image-20230605191601471](C:\Users\86178\AppData\Roaming\Typora\typora-user-images\image-20230605191601471.png)

