# -*- coding: utf-8 -*-
from app.utils import db
from .base_admin_model import BaseModelView


class Catagory(db.Model):
    # 表名
    __tablename__ = 'catagory'
    id = db.Column(db.Integer(), primary_key=True, index=True)
    name = db.Column(db.String(128), nullable=False, comment='名称')
    level = db.Column(db.Integer(), nullable=False, server_default='1', comment='层级')
    parent_id = db.Column(db.Integer(), db.ForeignKey('catagory.id'), comment='父ID')
    parent_catagory = db.relationship('Catagory', backref='child', remote_side=[id])  # 自关联
    status = db.Column(db.Integer(), nullable=False, server_default='1', comment='状态')
    # 外键
    goods = db.relationship('Goods', backref='catagory')


class AdminCatagory(BaseModelView):
    column_labels = dict(
        id='编号',
        name='名称',
        level='层级',
        status='状态',
        goods='相关商品',
        parent_catagory='父类别',
        child='子类别',
    )
