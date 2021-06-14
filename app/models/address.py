# -*- coding: utf-8 -*-
from app.utils import db
from .base_admin_model import BaseModelView


class Address(db.Model):
    # 表名
    __tablename__ = 'address'
    id = db.Column(db.Integer(), primary_key=True, index=True)
    area = db.Column(db.String(128), nullable=False, comment='地区名称')
    info = db.Column(db.String(128), nullable=False, comment='详细地址')
    zip_code = db.Column(db.String(128), comment='邮政编码')
    name = db.Column(db.String(128), nullable=False, comment='收件人姓名')
    phone = db.Column(db.String(32), nullable=False, comment='收件人手机号')
    address_name = db.Column(db.String(128), nullable=False, comment='地址备注')
    # 外键
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), comment='用户ID')
    orders = db.relationship('Order', backref='address')


class AdminAddress(BaseModelView):
    column_labels = dict(
        id='编号',
        area='地区名称',
        info='详细地址',
        zip_code='邮政编码',
        name='收件人姓名',
        phone='收件人手机号',
        address_name='地址备注',
        user='用户',
        orders='相关订单',
    )
