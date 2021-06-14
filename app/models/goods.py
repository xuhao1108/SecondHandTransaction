# -*- coding: utf-8 -*-
import os
from datetime import datetime
from sqlalchemy.sql import func
from jieba.analyse.analyzer import ChineseAnalyzer
from flask_admin.form.upload import ImageUploadField

from app.configs import Constant
from app.utils import db
from .base_admin_model import BaseModelView

# 上传文件的字段
full_path = os.path.join(os.environ.get('UPLOAD_FOLDER'), 'goods/').replace('\\', '/')
base_path, save_path = full_path.split('/static/')
base_path += '/static/'


class Goods(db.Model):
    # 表名
    __tablename__ = 'goods'
    # 支持搜索的字段
    __searchable__ = ['title', 'info']
    # 中文分析
    __analyzer__ = ChineseAnalyzer()
    # 键
    id = db.Column(db.Integer(), primary_key=True, index=True)
    title = db.Column(db.String(128), nullable=False, comment='标题')
    info = db.Column(db.Text(), comment='简介')
    pictures = db.Column(db.Text(), nullable=False, comment='图片路径')
    # 总长度14位（整数12位，小数2位），保留2为小数
    price = db.Column(db.Float(precision='14,2'), nullable=False, comment='原价')
    sec_price = db.Column(db.Float(precision='14,2'), nullable=False, comment='二手价')
    condition = db.Column(db.Integer(), server_default='100', nullable=False, comment='新旧度')
    # 包邮、不包邮、其他（当面交易、电子发货）
    send_type = db.Column(db.String(128), nullable=False, comment='送货方式')
    send_price = db.Column(db.Float(precision='14,2'), nullable=False, comment='邮费')
    # 1：已发布，2：已出售，3：已下架
    status = db.Column(db.Integer(), server_default='1', nullable=False, comment='状态')
    published_time = db.Column(db.DateTime(timezone=True),
                               # server_default=func.now(),
                               default=datetime.utcnow, nullable=False, comment='发布时间')
    last_modify_time = db.Column(db.DateTime(timezone=True),
                                 # server_default=func.now(),
                                 default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment='最后修改时间')
    # 外键
    catagory_id = db.Column(db.Integer(), db.ForeignKey('catagory.id'), comment='类别ID')
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), comment='卖家ID')
    messages = db.relationship('Message', backref='goods')
    orders = db.relationship('Order', backref='goods')

    def get_parent_list(self, catagory, level=None):
        """
        获取当前类别的所有父类别信息
        :param catagory: 所有父类别信息
        :param level:
        :return:
        """
        if not level:
            for i in catagory:
                if self.catagory_id in catagory[i]:
                    level = i
                    break
        result = [
            catagory[level][self.catagory_id]['item']
        ]
        # 获取所有父类别信息
        self.get_info(catagory, level, self.catagory_id, result)
        # 反转数组，类别从大到小
        result.reverse()
        return result

    def get_info(self, catagory, level, c_id, result):
        """
        递归查找类别的父类别信息
        :param catagory: 所有类别
        :param level: 层级
        :param c_id: 当前类别id
        :param result: 结果集
        :return:
        """
        if c_id:
            # 获取当前层级选择的元素
            p_id = catagory[level][c_id]['parent_id']
            if p_id:
                # 将父类别信息添加到列表中
                result.append(catagory[level - 1][p_id]['item'])
                # 寻找父id的父id
                self.get_info(catagory, level - 1, p_id, result)

    def get_status(self):
        """
        获取商品状态
        :return:
        """
        flag = ''
        if self.status == Constant.GOODS_PUBLISHED:
            flag = '已发布'
        elif self.status == Constant.GOODS_CANCEL:
            flag = '已下架'
        elif self.status == Constant.GOODS_SOLD:
            flag = '已出售'
        return flag


class AdminGoods(BaseModelView):
    column_labels = dict(
        id='编号',
        title='标题',
        info='简介',
        price='原价',
        sec_price='二手价',
        condition='新旧度',
        send_type='送货方式',
        send_price='邮费',
        status='状态',
        published_time='发布时间',
        last_modify_time='最后修改时间',
        user='用户',
        catagory='类别',
        orders='订单',
        messages='消息',
        pictures='图片',
    )

    # form_extra_fields = {
    #     'pictures': ImageUploadField(label='图片')#, base_path=base_path,
    #                                  # namegen=lambda obj, file_data: '{}{}/{}'.format(save_path, file_data.filename)),
    # }
