# -*- coding: utf-8 -*-
import os
import re
import time
from flask import Blueprint, render_template, url_for, redirect, flash, current_app, request, session, jsonify, abort
from flask_login import login_user, logout_user, login_required, current_user

from app.configs import Constant
from app.models import User
from app.forms import FormProfile
from app.utils import send_mail, login_manager, db, get_verification_code, flash_form_errors, check_code
from .goods import get_goods_info

bp_user = Blueprint('user', __name__)


@bp_user.route('/register', methods=['GET', 'POST'])
def register():
    """
    用户注册页面
    :return:
    """
    # 提交表单
    if request.method == 'POST':
        # 获取表单数据
        form_email = request.form.get('email')
        form_code = request.form.get('verification_code')
        # 判断用户是否存在
        user = User.query.filter_by(email=form_email).first()
        if user:
            flash('用户已存在，请直接登录。')
            return redirect(url_for('.login'))
        # 获取session数据
        session_data = session.get(form_email, {}).get('register', {})
        verification_code = session_data.get('code')
        time_stamp = session_data.get('time_stamp', 0)
        expire_time = session_data.get('expire_time', 0)
        # 判断验证码是否过期
        if verification_code and time.time() - time_stamp > expire_time:
            flash('验证码已过期，请重试')
            return render_template('user/register.html', email=form_email)
        # 验证错误
        if str(form_code).lower() != str(verification_code).lower():
            flash('验证码错误，请重试')
            return render_template('user/register.html', email=form_email)
        # 验证正确
        user = User(email=form_email)
        try:
            # 删除session验证码
            session[form_email].pop('register')
        except:
            pass
        # 提交到数据库
        db.session.add(user)
        db.session.commit()
        # 登录用户
        login_user(user)
        # 重定向到next或跳转到个人页面
        return redirect(request.args.get('next') or url_for('.profile'))
    return render_template('user/register.html')


@bp_user.route('/login', methods=['GET', 'POST'])
def login():
    """
    用户登录页面
    :return:
    """
    # 若用户登录，返回个人页面
    if current_user.is_authenticated:
        return redirect(url_for('main.main'))
    # 提交表单
    if request.method == 'POST':
        # 获取表单数据
        form_email = request.form.get('email')
        form_tpye = request.form.get('type')
        form_password = request.form.get('password')
        form_code = request.form.get('verification_code')
        form_remember = request.form.get('remember')
        # 判断用户是否存在
        user = User.query.filter_by(email=form_email).first()
        if not user:
            flash('账号未注册，请先注册账号，然后在进行登录。')
            return redirect(url_for('.register'))
        # 密码登录
        if check_code(form_tpye, Constant.USER_PASSWORD_LOGIN):
            result = user.check_password(form_password)
            # 密码错误
            if not result:
                flash('密码错误，请重试。')
                return render_template('user/login.html', email=form_email)
        # 验证码登录
        elif check_code(form_tpye, Constant.USER_CODE_LOGIN):
            # 获取session数据
            session_data = session.get(form_email, {}).get(form_tpye, {})
            verification_code = session_data.get('code')
            time_stamp = session_data.get('time_stamp', 0)
            expire_time = session_data.get('expire_time', 0)
            # 判断验证码是否过期
            if time.time() - time_stamp > expire_time:
                flash('验证码已过期，请重试')
                return render_template('user/login.html', email=form_email)
            # 验证错误
            if str(form_code).lower() != str(verification_code).lower():
                flash('验证码错误，请重试')
                return render_template('user/login.html', email=form_email)
            try:
                # 删除session验证码
                session[form_email].pop('login_by_verification')
            except:
                pass
        else:
            flash('参数错误')
            return render_template('user/login.html')
        # 验证正确,登录用户
        login_user(user, remember=form_remember)
        # 重定向或跳转到个人页面
        return redirect(request.args.get('next') or url_for('main.main'))
    return render_template('user/login.html')


@bp_user.route('/ignore', methods=['GET', 'POST'])
def ignore():
    """
    用户找回密码页面
    :return:
    """
    # 提交表单
    if request.method == 'POST':
        # 获取表单数据
        email = request.form.get('email')
        result = send_user_email(email, Constant.USER_IGNORE_PASSSWORD, mode=Constant.TOKEN,
                                 endpoint='user.reset_password')
        # 用户不存在
        if check_code(result['code'], Constant.USER_NOT_EXIST):
            flash(result['message'])
            return redirect(url_for('.register'))
        # 已发送
        elif check_code(result['code'], Constant.SEND_CODE):
            flash(result['message'])
            return redirect(url_for('.login'))
        # 成功
        elif check_code(result['code'], Constant.SUCCESS):
            flash('找回密码邮件已发送，请注意查收。')
            return redirect(url_for('.login'))
    return render_template('user/ignore.html')


@bp_user.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    """
    修改密码页面
    :return:
    """
    token = request.args.get('token', '')
    # 解析token，获取邮件信息
    token_info = User.get_token_info(token)
    if not token_info:
        flash('验证已失效，请重新发送修改密码验证短信。')
        return redirect(url_for('.ignore'))
    email = token_info.get('email')
    _type = token_info.get('type')
    # 判断用户是否存在
    user = User.query.filter_by(email=email).first()
    if not user:
        flash('账号未注册，请直接注册。')
        return redirect(url_for('.register'))
    # 提交表单
    if request.method == 'POST':
        # 设置密码
        user.password = request.form.get('password')
        try:
            # 删除session验证码
            session[email].pop(_type)
        except:
            pass
        # 更新到数据库
        # db.session.add(user)
        db.session.commit()
        # 重定向到用户登录界面
        return redirect(url_for('.login'))
    return render_template('user/reset_password.html', token=token, email=email)


@bp_user.route('/send_verification_code', methods=['POST'])
def send_verification_code():
    """
    发送邮件验证码
    :return:
    """
    email = request.form.get('email')
    _type = request.form.get('type')
    mode = request.form.get('mode')
    endpoint = request.form.get('endpoint')
    expire_time = request.form.get('expire_time')
    # 发送邮件验证
    result = send_user_email(email, _type, mode, endpoint, expire_time)
    return jsonify(result)


@bp_user.route('/<email>')
def item(email):
    """
    用户个人主页面
    :return:
    """
    # 判断用户是否存在
    user = User.query.filter_by(email=email).first()
    if not user:
        abort(404)
    # 分页显示用户出售中的商品
    pagination, goods_count = get_goods_info(user, get_cancel=0)
    return render_template('user/item.html', user=user, pagination=pagination, goods_count=goods_count)


@bp_user.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """
    用户个人资料页面
    :return:
    """
    form = FormProfile(email=current_user.email, name=current_user.name, info=current_user.info, age=current_user.age,
                       sex=current_user.sex)
    if request.method == 'POST':
        # 验证表单
        if form.validate_on_submit():
            # 头像文件
            f = form.portrait.data
            if f.filename:
                file_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'user/portrait')
                # 用户id.jpg
                file_name = '{}.{}'.format(current_user.id, f.filename.split('.')[-1])
                # 完整保存路径
                full_path = os.path.abspath(os.path.join(file_folder, file_name))
                # 保存到本地
                f.save(full_path)
                # 路径保存到数据库，static之前的路径不需要保存
                current_user.portrait = full_path[full_path.find('\\static\\') + 8:].replace('\\', '/')
            # 昵称，年龄，性别，简介
            current_user.name = form.name.data
            current_user.age = form.age.data
            current_user.sex = form.sex.data
            current_user.info = form.info.data
            # 更新到数据库
            # db.session.add(current_user)
            db.session.commit()
            flash('修改成功！')
            return redirect(url_for('.profile'))
        else:
            flash_form_errors(form)
    return render_template('user/profile.html', form=form)


@bp_user.route('/logout')
@login_required
def logout():
    """
    退出登录
    :return:
    """
    next = request.args.get('next')
    logout_user()
    flash('您已退出登录')
    return redirect(url_for('.login', next=next))


@login_manager.unauthorized_handler
def unauthorized():
    """
    用户虚拟id失效的回调
    :return:
    """
    flash('用户会话已失效，请重新登录。')
    return redirect(url_for('user.login', next=request.url))


def send_user_email(email, _type, mode=None, endpoint=None, _expire_time=None):
    """
    发送邮件验证码或邮件token
    :return:
    """
    # 判断用户是否存在
    user = User.query.filter_by(email=email).first()
    # 判断是否发送过验证码
    time_stamp = session.get(email, {}).get(_type, {}).get('time_stamp', 0)
    expire_time = session.get(email, {}).get(_type, {}).get('expire_time', Constant.CODE_EXPIRE_TIME)
    # 默认是验证码
    mode = mode if mode else Constant.CODE
    # 判断验证码是否过期
    if time.time() - time_stamp < expire_time:
        error_code = Constant.ERROR
        if check_code(mode, Constant.CODE):
            error_code = Constant.SEND_CODE
        elif check_code(mode, Constant.TOKEN):
            error_code = Constant.SEND_TOKEN
        # 已经发送过验证码
        return {
            'code': error_code,
            'status': 'error',
            'message': '已发送过验证码，请注意查收。注：验证码在{}分钟内有效。'.format(int(expire_time / 60)),
        }
    subject, template, expire_time = '', '', Constant.CODE_EXPIRE_TIME
    # 注册验证码
    if check_code(_type, Constant.USER_REGISTER):
        # 用户存在
        if user:
            return {
                'code': Constant.USER_EXIST,
                'status': 'error',
                'message': '用户已存在，请直接登录。',
            }
        subject, template, expire_time = '账号注册', 'mail/user/register', Constant.CODE_EXPIRE_TIME * 5
    # 登录验证码。找回密码、重置密码 验证码
    elif check_code(_type, [Constant.USER_CODE_LOGIN, Constant.USER_IGNORE_PASSSWORD, Constant.USER_RESET_PASSWORD]):
        # 用户不存在
        if not user:
            return {
                'code': Constant.USER_NOT_EXIST,
                'status': 'error',
                'message': '用户不存在，请先注册。',
            }
        if check_code(_type, Constant.USER_CODE_LOGIN):
            subject, template, expire_time = '账号登录', 'mail/user/login', Constant.CODE_EXPIRE_TIME
        elif check_code(_type, Constant.USER_IGNORE_PASSSWORD):
            subject, template, expire_time = '找回密码', 'mail/user/reset_password', Constant.TOKEN_EXPIRE_TIME
        elif check_code(_type, Constant.USER_RESET_PASSWORD):
            subject, template, expire_time = '重置密码', 'mail/user/reset_password', Constant.TOKEN_EXPIRE_TIME
    else:
        abort(400)
    # 过期时间
    expire_time = _expire_time if _expire_time else expire_time
    verification_code, token_url = None, None
    if check_code(mode, Constant.CODE):
        # 生成验证码
        verification_code = get_verification_code()
    elif check_code(mode, Constant.TOKEN):
        # 生成token
        token = user.generate_token(_type)
        token_url = url_for(endpoint, token=token, _external=True)
    # 发送验证码邮件
    send_mail(email, subject, template, title=subject, verification_code=verification_code, url=token_url,
              expire_time=expire_time)
    # 将验证码保存到session中
    session[email] = {
        _type: {
            'code': verification_code,
            'token': token_url,
            'time_stamp': int(time.time()),
            'expire_time': expire_time
        }
    }
    return {
        'code': Constant.SUCCESS,
        'status': 'success',
        'message': '验证码发送成功，请注意查收。',
    }
