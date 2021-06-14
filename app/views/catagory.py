# -*- coding: utf-8 -*-
import json
from flask import Blueprint

from app.models import Catagory

bp_catagory = Blueprint('catagory', __name__)


@bp_catagory.app_context_processor
def init_constant():
    """
    将类别信息传给所有模板
    :return:
    """
    # 分类排序，按照等级不同划分
    catagory = format_catagory()
    # 物品类别信息
    return dict(catagory=catagory)


def format_catagory():
    """
    格式化类别信息
    :return:
    """
    # item = {
    #     'parent': parent_id,
    #     'item': catagory,
    #     'child': [item1, item2],
    # }
    result = {
        # level: {
        #     c_id: item
        # }
    }
    # 获取最高层级
    max_level_catagory = Catagory.query.order_by(-Catagory.level).first()
    # 从最低的层级开始遍历
    for level in range(max_level_catagory.level, 0, -1):
        # 获取该层级的所有有效（status=1）记录
        current_level_list = Catagory.query.filter_by(level=level, status=1).all()
        for catagory in current_level_list:
            c_id = catagory.id
            p_id = catagory.parent_id or 0
            # 初始化当前层级和item
            if level not in result:
                result[level] = {}
            if c_id not in result[level]:
                result[level][c_id] = {
                    'parent_id': None,
                    'item': None,
                    'child': []
                }
            # 赋值
            result[level][c_id]['parent_id'] = p_id
            result[level][c_id]['item'] = {'name': catagory.name, 'id': c_id}
            # 初始化父层级和父item
            if level - 1 not in result:
                result[level - 1] = {}
            if p_id not in result[level - 1]:
                result[level - 1][p_id] = {
                    'parent_id': None,
                    'item': None,
                    'child': []
                }
            # 赋值
            result[level - 1][p_id]['child'].append(result[level][c_id])
    return result

# def format_catagory():
#     """
#     格式化类别信息
#     :return:
#     """
#     result = {
#         # level:{
#         #   p_id:[
#         #       {
#         #           'item': item
#         #           'child': [child1, child2]
#         #       }
#         #   ]
#         # }
#     }
#     # 获取最高层级
#     max_level_catagory = Catagory.query.order_by(-Catagory.level).first()
#     # 从最低的层级开始遍历
#     for level in range(max_level_catagory.level, 0, -1):
#         # 获取该层级的所有有效（status=1）记录
#         current_level_list = Catagory.query.filter_by(level=level, status=1).all()
#         for catagory in current_level_list:
#             # 层级
#             if level not in result:
#                 result[level] = {}
#             # 顶层元素父id为None，故格式化为0
#             c_id = catagory.id
#             p_id = catagory.parent_id if catagory.parent_id else 0
#             # 父id
#             if p_id not in result[level]:
#                 result[level][p_id] = {
#                     'item': None,
#                     'child': {}
#                 }
#             # 若不是末尾层级且有子节点
#             if level + 1 in result and c_id in result[level + 1]:
#                 # 设置拥有子节点的父节点为当前节点
#                 # 只需要名称和id信息即可
#                 result[level + 1][c_id]['item'] = {
#                     'id': catagory.id,
#                     'name': catagory.name,
#                 }
#                 # 添加链条
#                 result[level][p_id]['child'][c_id] = result[level + 1][c_id]
#             else:
#                 # 直接添加节点
#                 result[level][p_id]['child'][c_id] = {
#                     'item': {
#                         'id': catagory.id,
#                         'name': catagory.name
#                     },
#                     'child': {}
#                 }
#     return result
