# -*- coding: utf-8 -*-
import logging
# import re
from logging.handlers import RotatingFileHandler, SMTPHandler


def config_log(app):
    """
    初始化日志
    """
    logger = logging.getLogger()
    # 设置日志等级
    logging.basicConfig(level=app.config['LOG_LEVEL'])
    # 为全局的日志工具对象（flaskapp使用的）添加日志记录器
    logger.addHandler(get_file_handler(app))
    logger.addHandler(get_mail_handler(app))


def get_file_handler(app):
    """
    获取日志文件程序对象
    :param app:
    :return:
    """
    # 创建日志格式
    log_format = logging.Formatter(app.config['LOG_FORMAT'], app.config['LOG_TIME'])
    # 创建日志记录器
    hanlder = RotatingFileHandler(app.config['LOG_FILE'], maxBytes=1024 * 1024 * 1024, backupCount=100,
                                  encoding=app.config['LOG_ENCODE'])
    # hanlder = TimedRotatingFileHandler(Config.LOG_FILE, when='D', backupCount=365)
    # 修改日志后缀
    # hanlder.suffix = '%Y-%m-%d.log'
    # hanlder.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}(\.\w+)?$")
    # 设置等级
    hanlder.setLevel(logging.INFO)
    # 设置格式
    hanlder.setFormatter(log_format)
    return hanlder


def get_mail_handler(app):
    """
    获取日志邮件程序对象
    :param app:
    :return:
    """
    # 创建日志格式
    log_format = logging.Formatter(app.config['LOG_FORMAT'], app.config['LOG_TIME'])
    # 创建日志记录器
    hanlder = SMTPHandler((app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                          app.config['MAIL_USERNAME'], [app.config['FLASK_ADMIN']],
                          'Application Error', credentials=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']))
    # 设置等级
    hanlder.setLevel(logging.ERROR)
    # 设置格式
    hanlder.setFormatter(log_format)
    return hanlder
