# -*- coding: utf-8 -*-
import os
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSSerializer
from flask_admin.form.upload import ImageUploadField

from .message import association_table
from .base_admin_model import BaseModelView
from app.configs import Constant
from app.utils import db, login_manager

# 上传文件的字段
full_path = os.path.join(os.environ.get('UPLOAD_FOLDER'), 'user/portrait/').replace('\\', '/')
base_path, save_path = full_path.split('/static/')
base_path += '/static/'


class User(UserMixin, db.Model):
    # 表名
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True, index=True)
    email = db.Column(db.String(128), unique=True, index=True, nullable=False, comment='邮箱(账号)')
    name = db.Column(db.String(128), nullable=False, comment='昵称')
    _password = db.Column('password', db.String(128), comment='密码（加密后的）')  # 使数据库名称规范保持不变
    portrait = db.Column(db.Text(), nullable=False, server_default='img/default.jpg', comment='头像路径')
    age = db.Column(db.Integer(), comment='年龄')
    sex = db.Column(db.String(4), comment='性别')
    info = db.Column(db.Text(), comment='简介')
    # 外键
    type = db.Column(db.Integer(), db.ForeignKey('role.id'), server_default='1', comment='用户类型')
    address = db.relationship('Address', backref='user')
    goods = db.relationship('Goods', backref='user')
    send_messages = db.relationship('Message', backref='sender')
    receive_messages = db.relationship('Message', backref='receiver', secondary=association_table)

    @property
    def password(self):
        """
        密码不可读
        :return:
        """
        return Exception('密码不可读')

    @password.setter
    def password(self, password):
        """
        获取密码的hash值
        :param password:
        :return:
        """
        self._password = generate_password_hash(password)

    def check_password(self, password):
        """
        检查密码正确性
        :param password:
        :return:
        """
        return check_password_hash(self._password, password)

    def check_hash_password(self, hash_password):
        return self._password == hash_password

    def generate_token(self, _type=Constant.USER_IGNORE_PASSSWORD, expires_in=Constant.TOKEN_EXPIRE_TIME):
        """
        生成验证token
        :param _type: token类型
        :param expires_in: 过期时间
        :return:
        """
        # 创建序列化对象
        serializer = TJWSSerializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        # 返回 序列化的邮件参数
        return serializer.dumps({
            'type': _type,
            'email': self.email
        })

    @staticmethod
    def get_token_info(token):
        """
        解析token信息
        :param token: token
        :return:
        """
        # 创建序列化对象
        serializer = TJWSSerializer(current_app.config['SECRET_KEY'])
        try:
            # 返回 反序列化的邮件参数
            return serializer.loads(token)
        except:
            return ''

    def get_id(self, expires_in=Constant.USER_LOGIN_EXPIRE_TIME):
        """
        获取用户虚拟id
        :param expires_in: 过期时间，默认值：一个月
        :return: 序列化的 邮件和hash密码 值
        """
        # 创建序列化对象
        serializer = TJWSSerializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        # 返回 序列化的 邮件和hash密码 参数
        return serializer.dumps({
            'email': self.email,
            'hash_password': self._password
        })


class AdminUser(BaseModelView):
    # 这里是为了自定义显示的column名字
    column_labels = dict(
        id='编号',
        role='用户类型',
        email='邮箱(账号)',
        name='昵称',
        age='年龄',
        sex='性别',
        info='简介',
        address='收货地址',
        goods='出售的商品',
        buy_order='买家的订单',
        sell_order='卖家的订单',
        send_messages='发送的消息',
        receive_messages='接收的消息',
        receive_message='接收的消息',
    )

    # 如果不想显示某些字段，可以重载这个变量
    column_exclude_list = (
        '_password',
    )

    form_extra_fields = {
        'portrait': ImageUploadField(label='头像', base_path=base_path,
                                     namegen=lambda obj, file_data: '{}{}'.format(save_path, file_data.filename)),
    }

    # def __init__(self, session, **kwargs):
    #     super(AdminUser, self).__init__(User, session, **kwargs)


@login_manager.user_loader
def user_load(user_id):
    """
    根据虚拟id查找用户
    :param user_id:
    :return:
    """
    # 创建序列化对象
    serializer = TJWSSerializer(current_app.config['SECRET_KEY'])
    # 若用户虚拟id过期，则返回None
    try:
        # 反序列化的用户虚拟id
        data = serializer.loads(user_id)
        # 查找用户
        user = User.query.filter_by(email=data.get('email')).first()
        # 若序列化参数hash密码不一致，则返回None
        if user and user.check_hash_password(data.get('hash_password')):
            return user
        else:
            return None
    except:
        return None
