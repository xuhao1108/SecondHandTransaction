# -*- coding: utf-8 -*-
from flask import Flask
from .configs import config
from .models import config_admin_model
from .utils import config_extendsions, db, admin
from .views import config_blueprints


def create_app(config_name):
    """
    创建app
    :param config_name:
    :return:
    """
    # 创建应用实例
    app = Flask(__name__)
    # 初始化配置
    app.config.from_object(config[config_name])
    # 扩展
    config_extendsions(app)
    # 蓝本
    config_blueprints(app)
    # 后台管理
    config_admin_model(admin, db)
    # 创建数据库
    with app.app_context():
        db.create_all()
    return app
