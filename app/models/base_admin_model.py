# -*- coding: utf-8 -*-
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView


class BaseModelView(ModelView):
    # 这三个变量定义管理员是否可以增删改，默认为True
    # can_delete = False
    # can_edit = False
    # can_create = False
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role.name in ['admin', 'superAdmin']
