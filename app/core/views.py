# -*- coding=utf-8 -*-
from datetime import datetime

from flask import (
    Blueprint, jsonify, redirect,
    request, url_for, session, g,
)
from flask.ext.login import (
    current_user, current_app, logout_user,
    login_user, login_required, LoginManager,
)
from mongoengine import Q
from werkzeug.datastructures import MultiDict

from app.core.models import User
from app.core.forms import LoginForm, ResetPasswordForm, RegisterForm
from app.decorators import validate_form
from app.utils import (
    trim, get_token, api_ok, api_error
)

__all__ = ['user']

user = Blueprint('user', __name__)
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'user.login'
login_manager.login_message = None


@login_manager.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first()


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('user.login'))


@user.route("/")
@user.route("/user/login/", methods=["GET", "POST"])
@validate_form(LoginForm)
def login():
    form = g.form
    condition = Q(user_name=trim(form.user_name.data))
    user = User.objects.filter(condition).first()
    if user is None:
        return api_error(10001)

    if not user.check_password(trim(form.password.data)):
        return api_error(10002)

    if not (user.is_authenticated() and user.is_active()):
        return api_error(10003)

    remember_me = True if form.remember_me.data else False
    login_user(user, remember=remember_me)
    User.objects(id=user.id).update_one(last_login=datetime.utcnow())

    res = jsonify(code=0)
    res.set_cookie('token', get_token())
    return res


@user.route('/user/logout/', methods=["GET"])
@login_required
def logout():
    user_name = current_user.user_name
    logout_user()
    session.clear()

    current_app.logger.info('User %s logout' % user_name)

    res = jsonify(code=0)
    res.set_cookie('token', '', expires=0)
    return res


@user.route('/user/change_password/', methods=['POST'])
@login_required
@validate_form(ResetPasswordForm)
def change_password():
    form = g.form

    user = User.objects.filter(id=current_user.id).first()
    if user is None:
        return api_error(10005)

    if not user.check_password(form.old_password.data):
        return api_error(10006)

    user.change_password(form.new_password.data)
    user.save()
    return jsonify(success=True)



@user.route('/user/edit/', methods=['POST'])
@login_required
def edit_userinfo():
    pass


@user.route('/user/info/')
@login_required
def user_info():
    user_info = User.objects.filter(id=current_user.id).first()
    if user_info is None:
        return api_error(10008)

    return api_ok(data=dict(user_info=user_info))


@user.route('/user/register/', methods=['POST'])
@validate_form(RegisterForm)
def register():
    form = g.form
    condition = Q(user_name=form.user_name.data)
    if User.objects.filter(condition).first():
        return api_error(code=10009)

    obj = dict(
        user_name=form.user_name.data,
        password=form.password.data,
        email=form.email.data,
        phone=form.phone.data,
        first_name=form.first_name.data,
        last_name=form.last_name.data,
        full_name=form.full_name.data,
    )
    user = User.objects.create(**obj)
    user.change_password(form.password.data)
    user.save()

    return api_ok(data=dict(user=user))

