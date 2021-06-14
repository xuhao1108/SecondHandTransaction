# -*- coding: utf-8 -*-
import os
from flask_login import current_user
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.fileadmin.s3 import S3FileAdmin


class AdminView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role.name in ['admin', 'superAdmin']

    @expose('/')
    def index(self):
        return self.render('admin/main.html')


def add_file_view(admin):
    """
    后台管理
    :param admin:
    :return:
    """
    # 文件管理
    # admin.add_view(FileAdmin(os.environ.get('UPLOAD_FOLDER'), '/static/', name='文件'))
    pass
