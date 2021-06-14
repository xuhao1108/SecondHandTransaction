# -*- coding: utf-8 -*-
import os
import random
from flask import request

from app.configs import Constant


def get_verification_code(size=6, only_number=False, only_alph=False):
    """
    生成随机验证码
    :param size: 长度
    :param only_number: 仅数字
    :param only_alph: 仅字母
    :return:
    """
    code = ''
    for i in range(size):  # 循环4次
        index = random.randrange(0, 5)  # 生成0-6中的一个数
        number = str(random.randint(0, 9))  # 生成1-9的一个数字
        alph = chr(random.randint(65, 90))  # 生成A-Z中的大写字母
        if only_number:
            code += number
        elif only_alph:
            code += alph
        else:
            if index == i:
                code += number
            else:
                code += alph
    return code


def flash_form_errors(form):
    """
    显示表单错误
    :param form: 表单对象
    :return:
    """
    # 显示错误
    for error in form.errors:
        flash('，'.join(form.errors[error]))
        # flash('{}:{}'.format(error, form.errors[error]))


def check_code(code1, code2):
    """
    判断code是否一致，都转为str类型
    :param code1:
    :param code2:
    :return:
    """
    if isinstance(code2, list):
        return code1 in [str(x) for x in code2]
    return str(code1) == str(code2)


def get_upload_folder(upload_folder, end_path):
    """
    获取上传文件路径，若不存在，则创建
    :param upload_folder:
    :param end_path:
    :return:
    """
    file_folder = os.path.join(upload_folder, end_path)
    # 若路径不存在，则创建路径
    if not os.path.exists(file_folder):
        os.mkdir(file_folder)
    return {
        'full_file_folder': file_folder,
        'file_folder': file_folder[file_folder.find('\\static\\') + 8:].replace('\\', '/'),
        'file_name': []
    }


def get_pages(default_page=Constant.START_PAGE, default_per_page=Constant.PER_PAGE):
    """
    获取页码参数
    :param default_page: 默认起始页码
    :param default_per_page: 默认每页数量
    :return:
    """
    try:
        # 页码
        page = int(request.args.get('page', default_page))
        per_page = int(request.args.get('per_page', default_per_page))
        return {
            'page': page,
            'per_page': per_page,
        }
    except:
        return {
            'page': default_page,
            'per_page': default_per_page,
        }


def get_valid_dict(data):
    """
    删除无效的key
    :param data:
    :return:
    """
    pop_key = []
    for key in data:
        if not data[key]:
            pop_key.append(key)
    [data.pop(key) for key in pop_key]
    return data
