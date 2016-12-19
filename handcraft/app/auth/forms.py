# coding: utf-8
from flask_wtf import Form
from flask import flash
from wtforms import StringField, PasswordField, SubmitField, RadioField, SelectField
from wtforms.validators import DataRequired, Length, Email, Required, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User, Group

class LoginForm(Form):
    email = StringField(u'电子邮件',validators=[DataRequired(), Length(1, 64),Email()])
    password = PasswordField(u'密码',validators=[DataRequired()])

class RegistrationForm(Form):
    username = StringField('用户名',validators=[Required()])
    email = StringField(u'电子邮件',validators=[Required(), Length(1, 64),Email()])
    phone = StringField('手机',validators=[Required()])
    password = PasswordField('密码', validators=[Required(), EqualTo('password2', message='密码必须匹配.')])
    password2 = PasswordField('确认密码', validators=[Required()])
    role = SelectField('角色', choices=[('0', '超级管理员'), ('1', '部门管理员'), ('2', '普通用户')],validators=[Required()])
    group = StringField('用户组',validators=[Required()])
    active = StringField('状态',validators=[Required()])
    submit = SubmitField('提交')


    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            flash(u'邮箱地址已经存在', 'danger')
            #raise ValidationError('Email already registered.')
    
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            flash(u'该用户已经注册', 'danger')
            #raise ValidationError('Username already in use.')


class EmailForm(Form):
    email = StringField(u'电子邮件',validators=[DataRequired(), Length(1, 64),Email()])

class PasswordForm(Form):
    password = PasswordField(u'密码',validators=[DataRequired()])

class UserForm(Form):
    username = StringField('用户名',validators=[Required()])

class SettingForm(Form):
    id = StringField('id',validators=[Required()])
    username = StringField('用户名',validators=[Required()])
    email = StringField(u'电子邮件',validators=[Required(), Length(1, 64),Email()])
    phone = StringField('手机',validators=[Required()])
    role = SelectField('角色', choices=[('0', '超级管理员'), ('1', '部门管理员'), ('2', '普通用户')],validators=[Required()])
    submit = SubmitField('提交')

class GroupForm(Form):
    name = StringField('组名',validators=[Required()])
    comment = StringField('备注',validators=[Required()])
    submit = SubmitField('提交')
   
    def validate_name(self, field):
        if Group.query.filter_by(name=field.data).first():
            flash(u'该用户组已经注册', 'danger')

class EditorForm(Form):
    id = StringField('id',validators=[Required()])
    name = StringField('用户组',validators=[Required()])
    comment = StringField('备注',validators=[Required()])
    submit = SubmitField('提交')

class AvatarForm(Form):
    submit = SubmitField('提交')
