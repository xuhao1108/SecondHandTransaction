# -*- coding: utf-8 -*-
import os
from datetime import datetime
from sqlalchemy.sql import func
from flask_admin.form.upload import ImageUploadField

from app.utils import db
from .base_admin_model import BaseModelView

association_table = db.Table('receive_message',
                             db.Column('receiver_id', db.Integer(), db.ForeignKey('user.id'), nullable=False),
                             db.Column('receive_message_id', db.Integer(), db.ForeignKey('message.id'), nullable=False)
                             )

# 上传文件的字段
full_path = os.path.join(os.environ.get('UPLOAD_FOLDER'), 'message/').replace('\\', '/')
base_path, save_path = full_path.split('/static/')
base_path += '/static/'


class Message(db.Model):
    # 表名
    __tablename__ = 'message'
    id = db.Column(db.Integer(), primary_key=True, index=True)
    text = db.Column(db.Text(), nullable=False, comment='内容')
    pictures = db.Column(db.Text(), comment='图片路径')
    send_time = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False, comment='发送时间')
    message_type = db.Column(db.String(128), comment='类型')
    # 外键
    reply_message_id = db.Column(db.Integer(), db.ForeignKey('message.id'), comment='回复的信息ID')  # 回复的id
    reply_messages = db.relationship('Message', backref='reply', remote_side=[id])  # 自关联
    # ---
    goods_id = db.Column(db.Integer(), db.ForeignKey('goods.id'), comment='商品ID')
    sender_id = db.Column(db.Integer(), db.ForeignKey('user.id'), comment='发送者ID')
    receivers = db.relationship('User', backref='receive_message', secondary=association_table)


class AdminMessage(BaseModelView):
    column_labels = dict(
        id='编号',
        text='内容',
        send_time='发送时间',
        message_type='类型',
        reply_messages='回复的信息',
        receivers='接收者',
        receiver='接收者',
        sender='发送者',
        buy_order='买家的订单',
        sell_order='卖家的订单',
        goods='商品',
        reply='回复的信息',
        pictures='图片',
    )

    # form_extra_fields = {
    #     'pictures': ImageUploadField(label='图片')# , base_path=base_path,
    #                                  # namegen=lambda obj, file_data: '{}/{}'.format(save_path, file_data.filename)),
    # }
