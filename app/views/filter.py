# -*- coding: utf-8 -*-
import os
import json
from flask import Blueprint

bp_filter = Blueprint('filter', __name__)


@bp_filter.app_template_filter('pop_keys')
def pop_keys(data, *arg):
    """
    从字典中删除若干参数
    :return:
    """
    for key in arg:
        try:
            data.pop(key)
        except:
            pass
    return data


@bp_filter.app_template_filter('loads_pictures_info')
def loads_pictures_info(pictures_info):
    """
    解析数据库中的存放图片路径的json数据
    :return:
    """
    try:
        data = json.loads(pictures_info)
        path_list = [os.path.join(data['file_folder'], x).replace('\\', '/') for x in data['file_name']]
        return path_list
    except:
        return []
