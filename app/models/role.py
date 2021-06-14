# -*- coding: utf-8 -*-
from app.utils import db
from .base_admin_model import BaseModelView


class Role(db.Model):
    # 表名
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True, index=True)
    name = db.Column(db.String(128), nullable=False, comment='名称')
    status = db.Column(db.Integer(), nullable=False, server_default='1', comment='状态')
    # 外键
    users = db.relationship('User', backref='role')


class AdminRole(BaseModelView):
    can_delete = False
    can_edit = False
    can_create = False
    # 这里是为了自定义显示的column名字
    column_labels = dict(
        id='编号',
        name='名称',
        status='状态',
        users='用户'
    )
