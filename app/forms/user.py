# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, TextAreaField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Email, NumberRange, AnyOf
from flask_wtf.file import FileRequired, FileAllowed


class FormRegister(FlaskForm):
    """
    注册表单
    """
    email = EmailField('邮箱', validators=[DataRequired(message='邮箱不能为空！'),
                                         Email(message='请输入有效的邮箱地址！')])
    verification_code = StringField('验证码', validators=[DataRequired(message='验证码不能为空！')])
    submit = SubmitField('提交')


class FormProfile(FlaskForm):
    """
    个人信息表单
    """
    portrait = FileField('上传头像', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], message='请上传图片文件！')])
    email = EmailField('邮箱', validators=[DataRequired(message='邮箱不能为空！'),
                                         Email(message='请输入有效的邮箱地址！')])
    name = StringField('昵称', validators=[Length(2, 16, '昵称长度必须在2-16之间！')])
    age = SelectField('年龄', choices=[int(x) for x in range(100)], validators=[NumberRange(0, 100, '请选择有效的年龄！')],
                      coerce=int)
    sex = SelectField('性别', choices=['保密', '男', '女', '其他'],
                      validators=[AnyOf(['保密', '男', '女', '其他'], '请选择有效的性别！')])
    info = TextAreaField('简介', validators=[Length(max=128, message='个人简介最多128个字')])
    submit = SubmitField('提交')
