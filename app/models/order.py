# -*- coding: utf-8 -*-
from datetime import datetime
from sqlalchemy.sql import func

from app.configs import Constant
from app.utils import db
from .base_admin_model import BaseModelView


class Order(db.Model):
    # 表名
    __tablename__ = 'order'
    id = db.Column(db.Integer(), primary_key=True, index=True)
    booking_time = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False, comment='下单时间')
    pay_time = db.Column(db.DateTime(), comment='支付时间')
    send_time = db.Column(db.DateTime(), comment='发货时间')
    price = db.Column(db.Float(precision='14,2'), nullable=False, comment='总价')
    status = db.Column(db.Integer(), nullable=False, comment='状态')
    remark = db.Column(db.Text(), comment='备注')
    send_type = db.Column(db.String(128), nullable=False, comment='发货方式')
    send_name = db.Column(db.String(128), comment='快递名称')
    send_id = db.Column(db.String(128), comment='快递单号')
    # 外键
    goods_id = db.Column(db.Integer(), db.ForeignKey('goods.id'), comment='商品ID')
    # -------------
    buyer_id = db.Column(db.Integer(), db.ForeignKey('user.id'), comment='买家ID')
    seller_id = db.Column(db.Integer(), db.ForeignKey('user.id'), comment='卖家ID')
    # -
    buyer = db.relationship('User', backref='buy_order', foreign_keys='Order.buyer_id')
    seller = db.relationship('User', backref='sell_order', foreign_keys='Order.seller_id')
    # -------------
    buyer_message_id = db.Column(db.Integer(), db.ForeignKey('message.id'), comment='买家评论ID')
    seller_message_id = db.Column(db.Integer(), db.ForeignKey('message.id'), comment='卖家评论ID')
    # -
    buyer_message = db.relationship('Message', backref='buy_order', foreign_keys='Order.buyer_message_id')
    seller_message = db.relationship('Message', backref='sell_order', foreign_keys='Order.seller_message_id')
    # -------------
    address_id = db.Column(db.Integer(), db.ForeignKey('address.id'), comment='收货地址ID')

    def get_status(self):
        """
        获取订单状态
        :return:
        """
        flag = ''
        if self.status == Constant.ORDER_NO_PAY:
            flag = '待付款'
        elif self.status == Constant.ORDER_PAY:
            flag = '已付款'
        elif self.status == Constant.ORDER_NO_SEND:
            flag = '待发货'
        elif self.status == Constant.ORDER_SEND:
            flag = '已发货'
        elif self.status == Constant.ORDER_RECEIVE:
            flag = '确认收货'
        elif self.status == Constant.ORDER_NO_COMMENT:
            flag = '待评价'
        elif self.status == Constant.ORDER_BUYER_NO_COMMENT:
            flag = '买家待评价'
        elif self.status == Constant.ORDER_SELLER_NO_COMMENT:
            flag = '卖家待评价'
        elif self.status == Constant.ORDER_COMMENT:
            flag = '已评价'
        elif self.status == Constant.ORDER_BUYER_COMMENT:
            flag = '买家已评价'
        elif self.status == Constant.ORDER_SELLER_COMMENT:
            flag = '卖家已评价'
        elif self.status == Constant.ORDER_CANCEL:
            flag = '已取消'
        elif self.status == Constant.ORDER_REIMBURSE:
            flag = '已退款'
        return flag


class AdminOrder(BaseModelView):
    column_labels = dict(
        id='编号',
        booking_time='下单时间',
        pay_time='支付时间',
        send_time='发货时间',
        price='总价',
        status='备注',
        remark='状态',
        send_type='发货方式',
        send_name='快递名称',
        send_id='快递单号',
        goods='商品',
        address='收货地址',
        buyer='买家',
        seller='卖家',
        buyer_message='买家评论',
        seller_message='卖家评论',
    )
