# -*- coding: utf-8 -*-
import os
import json
from datetime import datetime
from flask import Blueprint, render_template, url_for, redirect, flash, current_app, request, abort
from flask_login import login_required, current_user
from sqlalchemy import or_

from app.configs import Constant
from app.forms import FormSend, FormComment
from app.models import Order, Goods, Message
from app.utils import db, flash_form_errors, check_code, get_upload_folder, get_pages

bp_order = Blueprint('order', __name__)


@bp_order.route('/')
@login_required
def main():
    """
    订单主页面
    :return:
    """
    # 过滤参数
    if check_code(request.args.get('seller', ''), 1):
        filters = [Order.seller_id == current_user.id]
    else:
        filters = [Order.buyer_id == current_user.id]
    if request.args.get('status'):
        filters.append(Order.status == request.args.get('status'))
    # 页码参数
    pages = get_pages(default_per_page=Constant.ORDER_PER_PAGE)
    pagination = Order.query.filter(*filters).order_by(-Order.booking_time).paginate(**pages)
    return render_template('order/main.html', pagination=pagination)


@bp_order.route('/<int:order_id>')
@login_required
def item(order_id):
    """
    订单详情页面
    :param order_id: 订单id
    :return:
    """
    filters = [Order.id == order_id, or_(Order.buyer_id == current_user.id, Order.seller_id == current_user.id)]
    order = Order.query.filter(*filters).first()
    # 找不到资源
    if not order:
        abort(404)
    return render_template('order/item.html', order=order)


@bp_order.route('/delete/<int:order_id>')
@login_required
def delete(order_id):
    """
    删除订单
    :param order_id: 订单id
    :return:
    """
    # TODO 删除订单
    return '未开放删除功能'
    # order1 = Order.query.filter_by(id=order_id, buyer_id=current_user.id).first()
    # order2 = Order.query.filter_by(id=order_id, seller_id=current_user.id).first()
    # order = order1 or order2
    # # 找不到资源
    # if not order:
    #     abort(404)
    # db.session.delete(order)
    # db.session.commit()
    # flash('删除成功！')
    # return redirect(request.args.get('next') or url_for('.main'))


@bp_order.route('/change_status/<int:order_id>')
@login_required
def change_status(order_id):
    """
    修改订单状态
    :param order_id: 订单id
    :return:
    """
    order = Order.query.filter_by(id=order_id, buyer_id=current_user.id).first()
    # 找不到资源
    if not order:
        abort(404)
    status = request.args.get('status')
    # 参数有误
    if not check_code(status, Constant.ORDER_ARGS):
        abort(400)
    if check_code(order.status, status):
        flash('当前已经是“{}”状态，无需重复操作！'.format(order.get_status()))
    else:
        # 参数为付款状态
        flag = None
        if check_code(status, Constant.ORDER_PAY):
            # 修改商品状态为已出售
            goods = Goods.query.filter_by(id=order.goods_id).first()
            # 找不到资源
            if not goods:
                abort(404)
            print(goods.status)
            goods.status = Constant.GOODS_SOLD
            # 已付款后，状态应为待发货
            status = Constant.ORDER_NO_SEND
            flag = '付款'
        order.status = status
        # db.session.add(order)
        db.session.commit()
        flash('{}成功！'.format(flag or order.get_status().replace('已', '')))
    return redirect(request.args.get('next') or url_for('.main'))


@bp_order.route('/pay/<int:order_id>')
@login_required
def pay(order_id):
    """
    支付订单
    :param order_id: 订单id
    :return:
    """
    # TODO 支付界面
    order = Order.query.filter_by(id=order_id, buyer_id=current_user.id).first()
    # 找不到资源
    if not order:
        abort(404)
    # 未付款状态
    if check_code(order.status, Constant.ORDER_NO_PAY):
        # # 修改订单为支付状态
        # order.status = Constant.ORDER_PAY
        # # 下单时间
        # order.pay_time = datetime.utcnow()
        # # 修改商品为已出售状态
        # goods = Goods.query.filter_by(id=order.goods_id).first()
        # # 找不到资源
        # if not goods:
        #     abort(404)
        # goods.status = Constant.GOODS_SOLD
        # # db.session.add(order)
        # db.session.commit()
        return render_template('order/pay.html', order=order)
    # 已付款
    flash('您已经付过款了！')
    return redirect(url_for('.item', order_id=order_id))


@bp_order.route('/send/<int:order_id>', methods=['GET', 'POST'])
@login_required
def send(order_id):
    """
    订单发货
    :param order_id: 订单id
    :return:
    """
    order = Order.query.filter_by(id=order_id, seller_id=current_user.id).first()
    # 找不到资源
    if not order:
        abort(404)
    # 未付款
    if check_code(order.status, Constant.ORDER_NO_PAY):
        flash('请等待买家付款后，您才可以发货！')
        return redirect(url_for('.item', order_id=order_id))
    # 已发货
    elif not check_code(order.status, Constant.ORDER_NO_SEND):
        flash('您已经发货了，请勿重新操作！')
        return redirect(url_for('.item', order_id=order_id))
    form = FormSend()
    if request.method == 'POST':
        if form.validate_on_submit():
            # 更新订单的发货信息
            order.send_name = form.send_name.data
            order.send_id = form.send_id.data
            order.send_time = datetime.utcnow()
            # 状态为已发货状态
            order.status = Constant.ORDER_SEND
            # db.session.add(order)
            db.session.commit()
            flash('发货成功！')
            return redirect(url_for('.main', seller=1))
        flash_form_errors(form)
    return render_template('order/send.html', form=form, order=order)


@bp_order.route('/comment/<int:order_id>', methods=['GET', 'POST'])
@login_required
def comment(order_id):
    """
    评论订单
    :param order_id: 订单id
    :return:
    """
    filters = [Order.id == order_id, or_(Order.buyer_id == current_user.id, Order.seller_id == current_user.id)]
    order = Order.query.filter(*filters).first()
    # 找不到资源
    if not order:
        abort(404)
    # 已经评论过了
    if order.buyer_id == current_user.id and order.buyer_message_id \
            or order.seller_id == current_user.id and order.seller_message_id:
        flash('您已经评论过了！')
        return redirect(url_for('.item', order_id=order_id))
    form = FormComment()
    if request.method == 'POST':
        if form.validate_on_submit():
            # 创建评论信息
            message = Message()
            message.text = form.comment.data
            message.message_type = Constant.MESSAGE_COMMENT
            message.goods_id = order.goods_id
            message.sender_id = current_user.id
            # 提交到数据库，获取数据id
            db.session.add(message)
            db.session.commit()
            # 处理并保存上传的图片文件
            pictures_info = get_upload_folder(current_app.config['UPLOAD_FOLDER'], 'message/')
            for index, file in enumerate(request.files.getlist('pictures')):
                # 不上传文件，会有一个文件名为空的文件对象
                if file.filename:
                    # 文件名格式：数据id-图片下标.文件后缀
                    file_suffix = file.filename.split('.') if '.' in file.filename else ['jpg']
                    file_name = '{}-{}.{}'.format(message.id, index + 1, file_suffix[-1])
                    pictures_info['file_name'].append(file_name)
                    # 保存到本地
                    file.save(os.path.abspath(os.path.join(pictures_info['full_file_folder'], file_name)))
            # 若有文件，则保存；否则不保存
            if pictures_info['file_name']:
                message.pictures = json.dumps(pictures_info)
            # 再次提交完整数据到数据库
            # db.session.add(message)
            db.session.commit()
            seller = 0
            # 修改评论状态
            # 买家评论
            if order.buyer_id == current_user.id:
                # 更新订单评论
                order.buyer_message_id = message.id
                # 买家卖家都没有评论
                if order.status == Constant.ORDER_RECEIVE:
                    # 状态为卖家待评论状态
                    order.status = Constant.ORDER_SELLER_NO_COMMENT
                # 卖家已评论，买家未评论
                elif order.status == Constant.ORDER_BUYER_NO_COMMENT:
                    # 状态为家待评论状态
                    order.status = Constant.ORDER_COMMENT
            # 卖家评论
            # if order.buyer_id == current_user.id:
            else:
                seller = 1
                # 更新订单评论
                order.seller_message_id = message.id
                # 买家卖家都没有评论
                if order.status == Constant.ORDER_RECEIVE:
                    # 状态为卖家待评论状态
                    order.status = Constant.ORDER_BUYER_NO_COMMENT
                # 买家已评论，卖家未评论
                elif order.status == Constant.ORDER_SELLER_NO_COMMENT:
                    # 状态为家待评论状态
                    order.status = Constant.ORDER_COMMENT
            # 提交到数据库
            # db.session.add(order)
            db.session.commit()
            flash('评论成功！')
            if seller:
                return redirect(url_for('.main', seller=1))
            return redirect(url_for('.main'))
        flash_form_errors(form)
    return render_template('order/comment.html', form=form, order=order)
