# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, TextAreaField
# from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length  # , Email, NumberRange, AnyOf
from flask_wtf.file import FileAllowed  # ,FileRequired


class FormSend(FlaskForm):
    """
    商品订单发货表单
    """
    send_name = StringField('快递名称', validators=[DataRequired('请填写快递名称！')])
    send_id = StringField('快递单号', validators=[DataRequired('请填写快递单号！')])
    submit = SubmitField('提交')


class FormComment(FlaskForm):
    """
    商品订单发货表单
    """
    comment = TextAreaField('评论', validators=[Length(max=65535, message='评论内容最多65535个字！')])
    pictures = FileField('图片', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], message='请上传图片文件！')])
    submit = SubmitField('提交')
