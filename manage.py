import os
from flask_script import Manager
from flask_migrate import MigrateCommand

from app import create_app
# 引入模型后，才会创建模型类
from app.models import *

# 获取应用实例
app = create_app(os.environ.get('FLASK_CONFIG') or 'default')

# 创建manger，可以通过shell操作app
manager = Manager(app)
# 添加shell命令
# 1. 初始化数据迁移的目录
# python manage.py db init
# 2. 数据库的数据迁移版本初始化
# python manage.py db migrate
# 3. 升级版本[创建表]
# python manage.py db upgrade
# 4. 降级版本[删除表]
# python manage.py db downgrade
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    # python manage.py runserver
    manager.run()
