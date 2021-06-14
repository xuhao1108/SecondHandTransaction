# -*- coding: utf-8 -*-
import json
from flask import Blueprint, render_template

from app.configs import Constant
from app.models import Goods
from app.utils import get_pages
from .goods import get_filters, get_orders

bp_main = Blueprint('main', __name__)


@bp_main.route('/')
def main():
    """
    主页面
    :return:
    """
    filters = [Goods.status == Constant.GOODS_PUBLISHED]
    filters = get_filters(*filters)
    orders = get_orders()
    pages = get_pages(default_per_page=Constant.GOODS_PER_PAGE)
    pagination = Goods.query.filter(*filters).order_by(*orders).paginate(**pages)
    return render_template('main/main.html', pagination=pagination)


@bp_main.app_context_processor
def init_constant():
    """
    将常量、logo传给所有模板
    :return:
    """
    # 常量信息
    constant = json.dumps(Constant.get_dict())
    # LOGO
    logo = 'YXH'
    # 物品类别信息
    return dict(constant=constant, logo=logo)
