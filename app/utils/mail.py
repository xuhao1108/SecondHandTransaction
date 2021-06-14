# -*- coding: utf-8 -*-
from flask import current_app, render_template
from flask_mail import Message
from threading import Thread

from .extensions import mail


def async_task(app, message):
    """
    异步发送邮件
    :param app: app对象
    :param message: 邮件对象
    :return:
    """
    with app.app_context():
        mail.send(message)


def send_mail(to, subject, template, **kwargs):
    """
    异步发送邮件
    :param to:
    :param subject:
    :param template:
    :param kwargs:
    :return:
    """
    message = Message(subject=subject, sender=current_app.config['MAIL_USERNAME'], recipients=[to])
    template = template if '.' not in template else template[:template.find('.')]
    message.html = render_template(template + '.html', **kwargs)
    message.body = render_template(template + '.txt', **kwargs)
    # 应用程序上下文
    app = current_app._get_current_object()
    # 创建子线程
    t = Thread(target=async_task, args=[app, message])
    t.start()
    return t
