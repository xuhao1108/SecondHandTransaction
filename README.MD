```
1. 安装相关依赖
安装：pip install -r requirements.txt
导出：pip freeze > requirements.txt
2. 设置环境变量
SET xx=xx
......
3. 创建数据库
CREATE DATABASE graduation_thesis;
4. 运行app
python manage.py runserver
5. 执行sql文件 mysql –u root –proot use graduation_thesis source
   /models/catagory.sql 
```

```
GraduationThesis\
|----app\ # 项目代码主目录
|    |----configs\ # 配置
|    |----forms\ # 视图表单
|    |----models\ # 数据库模型
|    |----static\ # 静态文件
|    |    |----css\ # 样式表
|    |    |----fonts\ # 字体
|    |    |----icons\ # 图标
|    |    |----img\ # logo、icon等图片
|    |    |----js\ # 脚本文件
|    |    |----upload\ # 用户上传的文件目录
|    |----templates\ # 模板
|    |----utils\ # 工具和插件
|    |----views\ # 蓝图
|    |----__init__.py # 初始化app
|----log\ # 项目日志
|----migrations\ # 数据库迁移目录
|----requirements\ # 各环境的相关依赖说明
|----test\ # 测试文件
|----venv\ # 虚拟环境的相关依赖
|----whoosh\ # 保存中文搜索字典的目录
|----manage.py # app启动文件
|----README.MD # 项目说明文件
```

# 错误页（error.py）

## handle_400_error

参数错误

## handle_401_error

认证失败

## handle_403_error

拒绝请求

## handle_404_error

找不到资源

## handle_500_error

服务器错误

## handle_503_error

服务器超载

# 过滤器（filter.py）

## pop_keys

从字典中删除若干参数

## loads_pictures_info

解析数据库中的存放图片路径的json数据

# 主页（main.py）

## 主页（main）

http://127.0.0.1:5000/

## init_constant

将常量、logo传给所有模板

# 用户（user.py）

## 登录（login）

http://127.0.0.1:5000/user/login

## 注册（register）

http://127.0.0.1:5000/user/register

## 退出（logout）

http://127.0.0.1:5000/user/logout

## 忘记密码（ignore）

http://127.0.0.1:5000/user/ignore

## 修改密码（reset_password）

http://127.0.0.1:5000/user/reset_password

## 发送验证码（send_verification_code）

http://127.0.0.1:5000/user/send_verification_code

## 用户信息页（profile）

http://127.0.0.1:5000/user/profile

## 用户主页（item）

http://127.0.0.1:5000/user/<email>

# 地址（address.py）

## 我的地址簿（main）

http://127.0.0.1:5000/address

## 地址详情页（item）

http://127.0.0.1:5000/address/<address_id>

## 添加/修改地址（modify）

添加：http://127.0.0.1:5000/address/modify/0

修改：http://127.0.0.1:5000/address/modify/<address_id>

## 删除地址（delete）

http://127.0.0.1:5000/address/delete/<address_id>

# 类别（catagory.py）

## init_constant

将类别信息传给所有模板

# 商品（goods.py）

## 卖家中心（main）

http://127.0.0.1:5000/goods

## 商品搜索（search）

http://127.0.0.1:5000/goods/search

## 商品详情页（item）

http://127.0.0.1:5000/goods/<goods_id>

## 添加/修改商品（modify）

添加：http://127.0.0.1:5000/goods/modify/0

修改：http://127.0.0.1:5000/goods/modify/<goods_id>

## 删除商品（delete）

http://127.0.0.1:5000/goods/delete/<goods_id>

## 修改商品状态（change_status）

http://127.0.0.1:5000/goods/change_status/<goods_id>

## 购买商品（buy）

http://127.0.0.1:5000/goods/buy/<goods_id>

# 订单（order.py）

## 订单中心（main）

http://127.0.0.1:5000/order

## 订单详情页（item）

http://127.0.0.1:5000/order/<order_id>

## 删除订单（delete）

http://127.0.0.1:5000/order/delete/<order_id>

## 修改订单状态（change_status）

http://127.0.0.1:5000/order/change_status/<order_id>

## 订单支付（pay）

http://127.0.0.1:5000/order/pay/<order_id>

## 订单发货（send）

http://127.0.0.1:5000/order/send/<order_id>

## 订单评论（comment）

http://127.0.0.1:5000/order/comment/<order_id>