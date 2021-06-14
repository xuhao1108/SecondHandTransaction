# -*- coding: utf-8 -*-
import os
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_moment import Moment
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from flask_babelex import Babel
from flask_admin import Admin

import flask_whooshalchemyplus

from .log import config_log
from .admin import AdminView, add_file_view

# 创建相关扩展对象
bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
moment = Moment()
login_manager = LoginManager()
csrf = CSRFProtect()
session = Session()
babel = Babel()
admin = Admin(name='后台管理系统', template_mode='bootstrap3', index_view=AdminView())


def config_extendsions(app):
    """
    初始化相关扩展
    :param app:
    :return:
    """
    # 初始化相关扩展
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    session.init_app(app)
    babel.init_app(app)
    admin.init_app(app)
    add_file_view(admin)
    # 搜索
    flask_whooshalchemyplus.init_app(app)
    # 用户登录管理
    config_login_manager(config_login_manager)
    # 后台管理
    # config_admin(admin, db)
    # 初始化日志
    config_log(app)


def config_login_manager(manager):
    """
    初始化用户登录模块
    :param manager: 用户登录模块
    :return:
    """
    # 用户未登录时重定向的页面
    manager.login_view = 'user.login'
    # 用户未登录时提示信息
    manager.login_message = '请先登录，才有权限继续访问页面！'
    # 消息的类别，默认为"message"
    manager.login_message_category = 'info'
    # 重新登录
    manager.refresh_view = 'user.login'
    manager.needs_refresh_message = '为了保护您的帐户，请重新认证以访问此页面。'
    manager.needs_refresh_message_category = 'info'
    # 会话保护级别:None,basic,strong
    # 在 basic 模式下或会话是永久的，如果该标识未匹配，会话会简单地被标记为非活跃的，且任何需要活跃登入的东西会强制用户重新验证。（当然，你必须已经使用了活跃登入机制才能奏效。）
    # 在 strong 模式下的非永久会话，如果该标识未匹配，整个会话（记住的令牌如果存在，则同样）被删除。
    manager.session_protection = 'strong'
