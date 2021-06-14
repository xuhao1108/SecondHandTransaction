# -*- coding: utf-8 -*-
import os
import json
import logging
from redis import Redis
# from flask_session import RedisSessionInterface

from .constant import Constant


class Config(Constant):
    DEBUG = True
    # 中文
    BABEL_DEFAULT_LOCALE = 'zh_CN'
    # 秘钥
    SECRET_KEY = os.environ.get('SECRET_KEY')[2:-1]
    # bootstrap
    # 默认为False:从网络加载bootsrap，True:从本地加载bootsrap
    BOOTSTRAP_SERVE_LOCAL = True
    # null：采用flask默认的保存在cookie中；redis：保存在redis中；memcached：保存在memcache；filesystem：保存在文件；mongodb：保存在MongoDB；sqlalchemy：保存在关系型数据库
    # SESSION_TYPE = 'filesystem'
    SESSION_TYPE = os.environ.get('SESSION_TYPE')
    # 加盐
    # SESSION_USE_SIGNER = True
    # SECRET_KEY = os.urandom(24) if SESSION_USE_SIGNER else None
    # 数据库
    # MYSQL
    # MYSQL_CONFIG = {
    #     'user': 'root',
    #     'password': 'root',
    #     'host': 'localhost',
    #     'port': 3306,
    #     'database': 'graduation_thesis'
    # }
    MYSQL_CONFIG = json.loads(os.environ.get('MYSQL_CONFIG', '{}').replace("'", '"'))
    DATABASE_URI_STRING = 'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'
    SQLALCHEMY_DATABASE_URI = DATABASE_URI_STRING.format(**MYSQL_CONFIG)
    # 默认为True，会追踪对象的修改并发送信息，会消耗额外内存
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # REDIS
    REDIS_CONFIG = json.loads(os.environ.get('REDIS_CONFIG', '{}').replace("'", '"'))
    SESSION_REDIS = Redis(**REDIS_CONFIG) if SESSION_TYPE == 'redis' else None
    # 搜索
    WHOOSH_BASE = os.environ.get('WHOOSH_BASE')
    # 日志 FATAL/CRITICAL：致命的，危险的  ERROR：错误  WARNING：警告  INFO：信息  DEBUG：调试  NOTSET：没有设置
    LOG_FILE = os.environ.get('LOG_FILE')
    LOG_ENCODE = 'UTF-8'
    LOG_LEVEL = logging.DEBUG
    LOG_TIME = '%Y-%m-%d %H:%M:%S'
    LOG_FORMAT = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s'
    # 邮件
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = 465 if MAIL_USE_SSL else 25
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # 文件上传路径，上传大小限制
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')
    MAX_CONTENT_LENGTH = 1024 * 1024 * 10  # 3MB
    # 管理员
    FLASK_ADMIN = os.environ.get('FLASK_ADMIN')
