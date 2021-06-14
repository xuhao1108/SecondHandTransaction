# -*- coding: utf-8 -*-
from .config import Config


class Development(Config):
    # 查询时会显示原始SQL语句
    # SQLALCHEMY_ECHO = True
    Config.MYSQL_CONFIG['database'] = 'graduation_thesis_dev'
    SQLALCHEMY_DATABASE_URI = Config.DATABASE_URI_STRING.format(**Config.MYSQL_CONFIG)
