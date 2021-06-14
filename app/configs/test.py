# -*- coding: utf-8 -*-
from .config import Config


class Test(Config):
    DEBUG = True
    Config.MYSQL_CONFIG['database'] = 'graduation_thesis_test'
    SQLALCHEMY_DATABASE_URI = Config.DATABASE_URI_STRING.format(**Config.MYSQL_CONFIG)
