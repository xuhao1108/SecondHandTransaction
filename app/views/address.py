# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, url_for, redirect, flash, request, session, abort
from flask_login import login_required, current_user

from app.configs import Constant
from app.models import Address
from app.forms import FormAddress
from app.utils import db, get_pages

bp_address = Blueprint('address', __name__)


@bp_address.route('/')
@login_required
def main():
    """
    全部收货地址页面
    :return:
    """
    pages = get_pages(default_per_page=Constant.ADDRESS_PER_PAGE)
    # 分页显示
    pagination = Address.query.filter_by(user_id=current_user.id).paginate(**pages)
    return render_template('address/main.html', pagination=pagination)


@bp_address.route('/<int:address_id>')
@login_required
def item(address_id):
    """
    查看具体一个收货地址的详细信息
    :param address_id: 收货地址id
    :return:
    """
    try:
        item_page = int(request.args.get('item_page')) if request.args.get('item_page') else 1
        address = Address.query.filter_by(id=address_id, user_id=current_user.id).first()
        # 找不到资源
        if not address:
            abort(404)
        return render_template('address/item.html', address=address, item_page=item_page)
    except:
        abort(400)


@bp_address.route('/modify/<int:address_id>', methods=['GET', 'POST'])
@login_required
def modify(address_id):
    """
    添加/修改 收货地址页面
    :return:
    """
    # address_id == 0，则表示创建；不为空，则表示修改
    # 新增地址，表单为空
    if address_id == 0:
        flag = '添加'
        address = Address(user_id=current_user.id)
        form = FormAddress()
    # 修改地址，表单自动填充
    else:
        flag = '修改'
        address = Address.query.filter_by(id=address_id, user_id=current_user.id).first()
        # 找不到资源
        if not address:
            abort(404)
        form = FormAddress(area=address.area, info=address.info, zip_code=address.zip_code,
                           name=address.name, phone=address.phone, address_name=address.address_name)
    if request.method == 'POST':
        if form.validate_on_submit():
            # 将表单数据填充到数据库对象上
            address.area = form.area.data
            address.info = form.info.data
            address.zip_code = form.zip_code.data
            address.name = form.name.data
            address.phone = form.phone.data.replace(' ', '')
            # 默认地址名称
            if form.address_name.data:
                address.address_name = form.address_name.data
            else:
                address.address_name = '我的第{}个收货地址'.format(len(current_user.address) + 1)
            # 提交到数据库
            db.session.add(address)
            db.session.commit()
            flash('{}成功！'.format(flag))
            # 最后一页
            last_url = url_for('.main', page=len(current_user.address) // Constant.ADDRESS_PER_PAGE or 1)
            return redirect(request.args.get('next') or last_url)
        else:
            flash_form_errors(form)
    return render_template('address/modify.html', form=form, address=address)


@bp_address.route('/delete/<int:address_id>')
@login_required
def delete(address_id):
    """
    删除收货地址
    :return:
    """
    address = Address.query.filter_by(id=address_id, user_id=current_user.id).first()
    # 找不到资源
    if not address:
        abort(404)
    db.session.delete(address)
    db.session.commit()
    flash('删除成功！')
    return redirect(request.args.get('next') or url_for('.main'))
