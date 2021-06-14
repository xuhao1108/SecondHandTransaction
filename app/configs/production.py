# -*- coding: utf-8 -*-
from .config import Config
import logging


class Production(object):
    DEBUG = False
    LOG_LEVEL = logging.INFO
