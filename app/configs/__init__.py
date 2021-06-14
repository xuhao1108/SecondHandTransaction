# -*- coding: utf-8 -*-
from .constant import Constant
from .config import Config
from .production import Production
from .development import Development
from .test import Test

config = {
    'default': Development,
    'production': Production,
    'development': Development,
    'test': Test
}
