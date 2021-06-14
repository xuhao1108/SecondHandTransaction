# -*- coding: utf-8 -*-
from .role import Role, AdminRole
from .user import User, AdminUser
from .address import Address, AdminAddress
from .catagory import Catagory, AdminCatagory
from .goods import Goods, AdminGoods
from .order import Order, AdminOrder
from .message import Message, AdminMessage

models = [
    {'model_view': AdminRole, 'model': Role, 'name': '类型', 'category': '用户'},
    {'model_view': AdminUser, 'model': User, 'name': '用户', 'category': '用户'},
    {'model_view': AdminAddress, 'model': Address, 'name': '地址簿'},
    {'model_view': AdminCatagory, 'model': Catagory, 'name': '类别', 'category': '商品'},
    {'model_view': AdminGoods, 'model': Goods, 'name': '商品', 'category': '商品'},
    {'model_view': AdminOrder, 'model': Order, 'name': '订单', 'category': '商品'},
    {'model_view': AdminMessage, 'model': Message, 'name': '消息'},
]


def config_admin_model(admin, db):
    """
    配置后台管理的模型
    :param admin:
    :param db:
    :return:
    """

    # 管理各模块
    for item in models:
        admin.add_view(item['model_view'](item['model'], db.session, name=item['name'], category=item.get('category'),
                                          endpoint='config_{}'.format(item['model'].__tablename__)))
