# -*- coding: utf-8 -*-
import os
import json
import glob
import flask_whooshalchemyplus
from flask import Blueprint, render_template, url_for, redirect, flash, request, abort
from flask_login import login_required, current_user
from sqlalchemy import text

from app.configs import Constant
from app.models import Goods, Catagory, Address, Order
from app.forms import FormGoods, FormBuy
from app.utils import db, flash_form_errors, check_code, get_upload_folder, get_pages, get_valid_dict

bp_goods = Blueprint('goods', __name__)


@bp_goods.route('/')
@login_required
def main():
    """
    出售的商品页面（卖家中心）
    :return:
    """
    pagination, goods_count = get_goods_info()
    return render_template('goods/main.html', pagination=pagination, goods_count=goods_count)


@bp_goods.route('/search', methods=['GET', 'POST'])
def search():
    """
    查找商品
    :return:
    """
    if request.method == 'POST':
        args = request.args.to_dict()
        form = request.form.to_dict()
        try:
            # 删除验证参数
            form.pop('csrf_token')
            # 合并参数
            args.update(form)
            # 剔除无效参数
            args = get_valid_dict(args)
        except:
            pass
        return redirect(url_for('.search', **args))
    # 过滤参数
    status = Goods.status == Constant.GOODS_PUBLISHED
    filters = get_filters(status)
    # 关键词
    key = request.args.get('key', '')
    # 排序参数
    orders = get_orders()
    # 页码参数
    pages = get_pages()
    if key:
        # 建立索引
        flask_whooshalchemyplus.index_one_model(Goods)
        # 查找
        pagination = Goods.query.filter(*filters).whoosh_search(key).order_by(*orders).paginate(**pages)
    else:
        # 查找
        pagination = Goods.query.filter(*filters).order_by(*orders).paginate(**pages)
    return render_template('goods/search.html', pagination=pagination)


@bp_goods.route('/<int:goods_id>')
def item(goods_id):
    """
    查看具体一个商品的详细信息
    :param goods_id: 商品id
    :return:
    """
    goods = Goods.query.filter_by(id=goods_id).first()
    # 找不到资源
    if not goods:
        abort(404)
    return render_template('goods/item.html', goods=goods)


@bp_goods.route('/modify/<int:goods_id>', methods=['GET', 'POST'])
@login_required
def modify(goods_id):
    """
    发布/修改 商品页面
    :param goods_id: 商品id
    :return:
    """
    # goods_id == -1，则表示创建；不为空，则表示修改
    # 新增商品，表单为空
    if goods_id == 0:
        flag = '发布'
        goods = Goods(user_id=current_user.id)
        form = FormGoods()
    else:
        flag = '修改'
        goods = Goods.query.filter_by(id=goods_id, user_id=current_user.id).first()
        # 找不到资源
        if not goods:
            abort(404)
        form = FormGoods(catagory=goods.catagory_id, title=goods.title, info=goods.info,
                         price=goods.price, sec_price=goods.sec_price, condition=goods.condition,
                         send_type=goods.send_type, send_price=goods.send_price)
    if request.method == 'POST':
        if form.validate_on_submit():
            # 将表单数据填充到数据库对象上
            goods.catagory_id = form.catagory.data
            goods.title = form.title.data
            goods.info = form.info.data
            goods.pictures = '{}'
            goods.price = form.price.data
            goods.sec_price = form.sec_price.data
            goods.condition = form.condition.data
            goods.send_type = form.send_type.data
            goods.send_price = form.send_price.data
            goods.status = Constant.GOODS_PUBLISHED
            # 提交到数据库，获取插入的id
            db.session.add(goods)
            db.session.commit()
            # 若图片存在，则先删除修改之前的图片文件
            pictures_info = get_upload_folder(current_app.config['UPLOAD_FOLDER'], 'goods/{}'.format(goods.catagory_id))
            # 数据id-*.*
            glob_regex = os.path.abspath(os.path.join(pictures_info['full_file_folder'], '{}-*.*'.format(goods.id)))
            for filename in glob.glob(glob_regex):
                try:
                    os.remove(filename)
                except:
                    pass
            # 处理并保存上传的图片文件
            for index, file in enumerate(request.files.getlist('pictures')):
                # 文件名格式：数据id-图片下标.文件后缀
                file_suffix = file.filename.split('.') if '.' in file.filename else ['jpg']
                file_name = '{}-{}.{}'.format(goods.id, index + 1, file_suffix[-1])
                pictures_info['file_name'].append(file_name)
                # 保存到本地
                file.save(os.path.abspath(os.path.join(pictures_info['full_file_folder'], file_name)))
            goods.pictures = json.dumps(pictures_info)
            # 提交到数据库
            db.session.add(goods)
            db.session.commit()
            flash('{}成功！'.format(flag))
            # 最后一页
            last_url = url_for('.main', page=len(current_user.goods) // Constant.GOODS_PER_PAGE or 1)
            return redirect(request.args.get('next') or last_url)
        else:
            flash_form_errors(form)
    return render_template('goods/modify.html', form=form, goods=goods)


@bp_goods.route('/delete/<int:goods_id>')
@login_required
def delete(goods_id):
    """
    删除商品
    :return:
    """
    goods = Goods.query.filter_by(id=goods_id, user_id=current_user.id).first()
    # 找不到资源
    if not goods:
        abort(404)
    db.session.delete(goods)
    db.session.commit()
    flash('删除成功！')
    return redirect(request.args.get('next') or url_for('.main'))


@bp_goods.route('/change_status/<int:goods_id>')
@login_required
def change_status(goods_id):
    """
    修改商品状态
    :param goods_id: 商品id
    :return:
    """
    status = request.args.get('status')
    if not check_code(status, Constant.GOODS_ARGS):
        abort(400)
    goods = Goods.query.filter_by(id=goods_id, user_id=current_user.id).first()
    # 找不到资源
    if not goods:
        abort(404)
    if check_code(goods.status, status):
        flash('当前已经是“{}”状态，无需重复操作！'.format(goods.get_status()))
    else:
        goods.status = status
        # db.session.add(goods)
        db.session.commit()
        flash('{}成功！'.format(goods.get_status().replace('已', '')))
    return redirect(request.args.get('next') or url_for('.main'))


@bp_goods.route('/buy/<int:goods_id>', methods=['GET', 'POST'])
@login_required
def buy(goods_id):
    """
    商品购买页面
    :param goods_id:
    :return:
    """
    goods = Goods.query.filter_by(id=goods_id).first()
    # 找不到资源
    if not goods:
        abort(404)
    flag = goods.get_status()
    if check_code(goods.user_id, current_user.id):
        flag = '自己'
    if flag and goods.status != Constant.GOODS_PUBLISHED:
        flash('您不能购买{}的商品！'.format(flag))
        return redirect(url_for('main.main', goods_id=goods_id))
    # 查找用户收货地址
    address_list = Address.query.filter_by(user_id=current_user.id).all()
    # 表单
    form = FormBuy()
    # 填充表单
    choices = []
    check_address = []
    for address in address_list:
        choices.append((address.id, '{}({};{})'.format(address.address_name, address.area, address.info)))
        check_address.append(str(address.id))
    form.address.choices = choices
    if request.method == 'POST':
        if form.validate_on_submit:
            # 非法地址
            if str(form.address.data) not in check_address:
                abort(400)
            # 创建订单
            order = Order()
            order.status = Constant.ORDER_NO_PAY
            order.price = goods.sec_price + goods.send_price
            order.remark = form.remark.data
            order.send_type = goods.send_type
            order.goods_id = goods.id
            order.buyer_id = current_user.id
            order.seller_id = goods.user_id
            order.address_id = form.address.data
            # 提交到数据库
            db.session.add(order)
            db.session.commit()
            # 跳转到付款页面
            flash('下单成功！')
            return redirect(url_for('order.main'))
        flash_form_errors(form)
    return render_template('goods/buy.html', goods=goods, form=form)


def get_goods_info(user=current_user, get_cancel=1, filter_args=None, order_args=None):
    """
    获取用户的商品信息
    :param user: 用户
    :param get_cancel: 是否获取已下架产品
    :param filter_args: 过滤参数
    :param order_args: 排序参数
    :return:
    """
    if filter_args is None:
        filter_args = []
    if order_args is None:
        order_args = []
    filters = [Goods.user_id == user.id]
    if not get_cancel:
        filters.append(Goods.status != Constant.GOODS_CANCEL)
    filters = get_filters(*filters, *filter_args)
    orders = get_orders(*order_args)
    pages = get_pages(default_per_page=Constant.GOODS_PER_PAGE)
    pagination = Goods.query.filter(*filters).order_by(*orders).paginate(**pages)
    goods_count = {
        'publishd': Goods.query.filter_by(user_id=user.id, status=Constant.GOODS_PUBLISHED).count(),
        'cancel': Goods.query.filter_by(user_id=user.id, status=Constant.GOODS_CANCEL).count(),
        'sold': Goods.query.filter_by(user_id=user.id, status=Constant.GOODS_SOLD).count(),
    }
    return pagination, goods_count


def get_filters(*args):
    """
    获取查询的参数
    :return:
    """
    filters = list(args)
    # 原价
    if request.args.get('min_price'):
        filters.append(Goods.price >= request.args.get('min_price'))
    if request.args.get('max_price'):
        filters.append(Goods.price <= request.args.get('max_price'))
    # 二手价
    if request.args.get('min_sec_price'):
        filters.append(Goods.sec_price >= request.args.get('min_sec_price'))
    if request.args.get('max_sec_price'):
        filters.append(Goods.sec_price <= request.args.get('max_sec_price'))
    # 新旧程度
    if request.args.get('min_condition'):
        filters.append(Goods.condition >= request.args.get('min_condition'))
    if request.args.get('max_condition'):
        filters.append(Goods.condition <= request.args.get('max_condition'))
    # 送货方式
    if request.args.get('send_type'):
        filters.append(Goods.send_type == request.args.get('send_type'))
    # 送货价格
    if request.args.get('min_send_price'):
        filters.append(Goods.send_price >= request.args.get('min_send_price'))
    if request.args.get('max_send_price'):
        filters.append(Goods.send_price <= request.args.get('max_send_price'))
    # 类别
    if request.args.get('catagory_id'):
        filters.append(Goods.catagory_id == request.args.get('catagory_id'))
    # 用户
    if request.args.get('user_id'):
        filters.append(Goods.user_id == request.args.get('user_id'))
    return filters


def get_orders(*args):
    """
    获取排序参数
    :return:
    """
    default_orders = [
        'id', 'title', 'info', 'pictures',
        'price', 'sec_price', 'condition',
        'send_type', 'send_price', 'status',
        # 降序
        '-last_modify_time', '-published_time',
        'catagory_id', 'user_id'
    ]
    orders = list(args)
    for default_key in default_orders:
        # 获取排序的键名
        asc_key = default_key.replace('-', '')
        # 获取参数值
        data = request.args.get('_{}'.format(asc_key))
        if data:
            try:
                # 参数为正，则升序；为负，则降序。
                key_order = asc_key if int(float(data)) >= 1 else '-{}'.format(asc_key)
            except:
                # 默认排序方式
                key_order = default_key
            orders.append(text(key_order))
        else:
            if default_key.startswith('-'):
                orders.append(text(default_key))
    return orders
