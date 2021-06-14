# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
# from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length  # , Email, NumberRange, AnyOf
# from flask_wtf.file import FileRequired, FileAllowed


class FormAddress(FlaskForm):
    """
    收货地址表单
    """
    area = StringField('地址信息', validators=[DataRequired('请选择地址信息！')])
    info = TextAreaField('详细地址', validators=[DataRequired('请填写详细地址信息'), Length(1, 128, message='地址信息最多128个字！')])
    zip_code = StringField('邮政编码', validators=[Length(max=32, message='邮政编码最多32位！')])
    name = StringField('收货人姓名', validators=[DataRequired('请选择收货人姓名！'), Length(1, 128, message='收货人姓名最多128个字！')])
    phone = StringField('手机号码', validators=[DataRequired('请选择手机号码！'), Length(11, 32, message='手机号码长度为11~32位！')])
    address_name = StringField('地址备注', validators=[Length(max=32, message='地址备注最多32位！')])
    submit = SubmitField('提交')
