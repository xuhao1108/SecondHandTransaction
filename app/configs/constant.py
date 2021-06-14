# -*- coding: utf-8 -*-

class Constant(object):
    # --------------------操作--------------------
    # 操作成功
    SUCCESS = 0
    # 操作失败
    ERROR = -1

    # --------------------用户--------------------
    # 用户存在
    USER_EXIST = 1
    # 用户不存在
    USER_NOT_EXIST = 2
    # 用户注册操作
    USER_REGISTER = 3
    # 用户密码登陆操作
    USER_PASSWORD_LOGIN = 4
    # 用户验证码登陆操作
    USER_CODE_LOGIN = 5
    # 用户忘记密码操作
    USER_IGNORE_PASSSWORD = 6
    # 用户重置密码操作
    USER_RESET_PASSWORD = 7

    # --------------------验证--------------------
    # 验证码
    CODE = 8
    # TOKEN
    TOKEN = 9
    # 已经发送过验证码
    SEND_CODE = 10
    # 已经发送过token
    SEND_TOKEN = 11
    # 过期时间：60s
    CODE_EXPIRE_TIME = 60
    # 过期时间：2h
    TOKEN_EXPIRE_TIME = 60 * 60 * 2
    # 用户登录过期时间：
    USER_LOGIN_EXPIRE_TIME = 60 * 60 * 24 * 30

    # --------------------页码--------------------
    # 起始页码
    START_PAGE = 1
    # 每页数量
    PER_PAGE = 2
    # 地址页面的起始页码
    ADDRESS_PER_PAGE = 10
    # 商品页面的每页数量
    GOODS_PER_PAGE = 12
    # 订单页面的每页数量
    ORDER_PER_PAGE = 10

    # --------------------商品--------------------
    # 已发布
    GOODS_PUBLISHED = 12
    # 已下架
    GOODS_CANCEL = 13
    # 已出售
    GOODS_SOLD = 14
    GOODS_ARGS = [GOODS_PUBLISHED, GOODS_CANCEL, GOODS_SOLD]
    # 送货价格
    SEND_PRICE = 15

    # --------------------订单--------------------
    # 待付款
    ORDER_NO_PAY = 16
    # 已付款
    ORDER_PAY = 17
    # 待发货
    ORDER_NO_SEND = 18
    # 已发货
    ORDER_SEND = 19
    # 已收到货
    ORDER_RECEIVE = 20
    # 待评价
    ORDER_NO_COMMENT = 21
    ORDER_BUYER_NO_COMMENT = 22
    ORDER_SELLER_NO_COMMENT = 23
    # 已评价
    ORDER_COMMENT = 24
    ORDER_BUYER_COMMENT = 25
    ORDER_SELLER_COMMENT = 26
    # 已取消
    ORDER_CANCEL = 27
    # 已完成
    ORDER_OVER = 28
    # 已退款
    ORDER_REIMBURSE = 29
    ORDER_ARGS = [ORDER_NO_PAY, ORDER_PAY, ORDER_NO_SEND, ORDER_SEND, ORDER_RECEIVE, ORDER_NO_COMMENT,
                  ORDER_BUYER_NO_COMMENT, ORDER_SELLER_NO_COMMENT, ORDER_COMMENT, ORDER_BUYER_COMMENT,
                  ORDER_SELLER_COMMENT, ORDER_CANCEL, ORDER_REIMBURSE]

    # --------------------信息--------------------
    # 消息
    MESSAGE_NEWS = 30
    # 评论
    MESSAGE_COMMENT = 31
    # 留言
    MESSAGE_MESSAGE = 32
    # 通知
    MESSAGE_NOTICE = 33

    @staticmethod
    def get_dict():
        """
        将类对象的参数转为dict
        :return:
        """
        data = {}
        for key in Constant.__dict__:
            if not key.startswith('__') and key != 'get_dict':
                data[key] = Constant.__dict__[key]
        return data


