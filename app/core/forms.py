# -*- coding=utf-8 -*-

from flask.ext.login import current_user
from flask.ext.mongoengine.wtf import model_form
from flask_wtf import Form
from wtforms import (
    validators, StringField, PasswordField,
    BooleanField,
)
from wtforms.validators import (
    ValidationError, DataRequired,
    Length, EqualTo, Email,
)
from werkzeug import security

from app.core.models import User


class ResetPasswordForm(Form):
    old_password = PasswordField(label=u'原密码')
    new_password = PasswordField(
        label=u'新密码',
        validators=[
            DataRequired(message=u'新密码是必填的'),
            Length(6, 20, message=u'密码长度必须在 6-20 之间'),
            EqualTo('confirm_password', message=u'请确认新密码')
        ]
    )
    confirm_password = PasswordField(
        label=u'确认密码',
        validators=[
            DataRequired(message=u'确认密码是必填的'),
            Length(6, 20, message=u'密码长度必须在 6-20 之间'),
        ]
    )


class LoginForm(Form):
    user_name = StringField(
        label=u"用户名",
        validators=[
            DataRequired(message=u"请填写用户名"),
            Length(0, 50, message=u"用户名长度必须在 0-50 之间")
        ]
    )
    password = StringField(
        label=u'密码',
        validators=[
            DataRequired(message=u"请填写密码"),
        ]
    )
    remember_me = BooleanField(label=u"记住我")


_EditSelfForm = model_form(
    User,
    field_args={
        'full_name': {
            'validators': [validators.Length(max=40)]
        },
    }, only=['full_name', 'phone', 'email']
)


class UserEditSelfForm(_EditSelfForm):
    def validate_full_name(self, field):
        user = User.objects.filter(full_name=field.data).first()
        if user is not None:
            if current_user.is_anonymous():
                raise ValidationError('请重新登录')

            if user.id != current_user.id:
                raise ValidationError('姓名已存在')


class RegisterForm(Form):
    user_name = StringField(
        label=u'用户名',
        validators=[
            DataRequired(message=u"请填写用户名"),
            Length(0, 50, message=u"用户名长度必须在 0-50 之间")
        ]
    )
    first_name = StringField(
        label=u'名字',
        validators=[DataRequired(message=u"请填写名字")]
    )
    last_name = StringField(
        label=u'姓氏',
        validators=[DataRequired(message=u"请填写姓氏")]
    )
    full_name = StringField(
        label=u'全名',
        validators=[DataRequired(message=u"请填写全名")]
    )
    email = StringField(
        label=u'邮箱',
        validators=[
            DataRequired(message=u"请填写邮箱"),
            Email(message=u"请填写正确的邮箱格式")
        ]
    )
    phone = StringField(
        label=u'手机号码',
        validators=[DataRequired(message=u"请填写邮箱")]
    )
    password = PasswordField(
        label=u'密码',
        validators=[
            DataRequired(message=u'请填写密码'),
            EqualTo('confirm_password', message=u'请确认密码'),
            Length(6, 400, message=u'密码长度必须在 6-20 之间')
        ]
    )
    confirm_password = PasswordField(
        label=u'确认密码',
        validators=[
            DataRequired(message=u"请填写确认密码"),
            Length(6, 400, message=u'密码长度必须在 6-20 之间')
        ]
    )

    def validate_password(self, field):
        data = security.generate_password_hash(field.data)
        self.password.data = data
