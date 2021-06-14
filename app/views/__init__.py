# -*- coding: utf-8 -*-
from .error import bp_errors
from .filter import bp_filter
from .main import bp_main
from .user import bp_user
from .address import bp_address
from .catagory import bp_catagory
from .goods import bp_goods
from .order import bp_order

blueprints = [
    (bp_errors, ''),
    (bp_filter, ''),
    (bp_main, ''),
    (bp_user, '/user'),
    (bp_address, '/address'),
    (bp_catagory, '/catagory'),
    (bp_goods, '/goods'),
    (bp_order, '/order'),
]


def config_blueprints(app):
    """
    注册蓝图
    :param app:
    :return:
    """
    for blueprint, url_prefix in blueprints:
        app.register_blueprint(blueprint, url_prefix=url_prefix)
