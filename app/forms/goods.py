# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, FileField, TextAreaField, SelectField, IntegerField
# from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, NumberRange  # , Email, AnyOf
from flask_wtf.file import FileAllowed  # , FileRequired


class FormGoods(FlaskForm):
    """
    发布商品表单
    """
    catagory = StringField('类别', validators=[DataRequired('请选择类别！')])
    title = StringField('标题', validators=[DataRequired('请填写标题！'), Length(1, 128, message='请控制标题在1~128个字之间！')])
    info = TextAreaField('简介', validators=[Length(max=65535, message='简介内容最多65535个字！')])
    pictures = FileField('图片', validators=[DataRequired('至少上传一张图片！'),
                                           FileAllowed(['jpg', 'jpeg', 'png', 'gif'], message='请上传图片文件！')])
    price = IntegerField('原价', validators=[NumberRange(1, 10 ** 13 - 1, message='请控制商品原价在1~12位之间且为正数！（单位：人民币）')])
    sec_price = IntegerField('二手价（出售价格）',
                             validators=[NumberRange(1, 10 ** 13 - 1, message='请控制商品二手价在1~12位之间且为正数！（单位：人民币）')])
    condition = IntegerField('新旧度', default=99, validators=[NumberRange(1, 100, message='新旧度格式为1~100之间且为正数！')])
    send_type = RadioField('送货方式', choices=['包邮', '不包邮', '其他'], default='包邮', validators=[DataRequired('请选择送货方式！')])
    send_price = IntegerField('邮费', default=0,
                              validators=[NumberRange(0, 10 ** 13 - 1, message='请控制邮费在1~12位之间且为正数！（单位：人民币）')])
    submit = SubmitField('提交')


class FormBuy(FlaskForm):
    """
    购买商品表单
    """
    address = SelectField('收货地址', validators=[DataRequired('请选择收货地址！')])
    remark = TextAreaField('备注', validators=[Length(max=65535, message='备注内容最多65535个字！')])
    submit = SubmitField('购买')
