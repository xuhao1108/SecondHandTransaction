# -*- coding: utf-8 -*-
from flask import Blueprint, render_template

bp_errors = Blueprint('errors', __name__)


@bp_errors.app_errorhandler(400)
def handle_400_error(error):
    """
    参数错误
    :param error:
    :return:
    """
    return render_template('errors/400.html'), 400


@bp_errors.app_errorhandler(401)
def handle_401_error(error):
    """
    认证失败
    :param error:
    :return:
    """
    return render_template('errors/401.html'), 401


@bp_errors.app_errorhandler(403)
def handle_403_error(error):
    """
    拒绝请求
    :param error:
    :return:
    """
    return render_template('errors/403.html'), 403


@bp_errors.app_errorhandler(404)
def handle_404_error(error):
    """
    找不到资源
    :param error:
    :return:
    """
    return render_template('errors/404.html'), 404


@bp_errors.app_errorhandler(500)
def handle_500_error(error):
    """
    服务器错误
    :param error:
    :return:
    """
    return render_template('errors/500.html'), 500


@bp_errors.app_errorhandler(503)
def handle_503_error(error):
    """
    服务器超载
    :param error:
    :return:
    """
    return render_template('errors/503.html'), 503
