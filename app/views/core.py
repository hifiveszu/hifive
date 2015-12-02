# -*- coding=utf-8 -*-
from datetime import datetime

from flask import (
    Blueprint, jsonify, redirect,
    url_for, session, g,
)
from flask.ext.login import (
    current_user, current_app, logout_user,
    login_user, login_required, LoginManager,
)
from mongoengine import Q

from app.models import User
from app.forms.core import LoginForm, ResetPasswordForm, RegisterForm
from app.decorators import validate_form
from app.utils import (
    trim, get_token, ok_jsonify, fail_jsonify, codes
)

__all__ = ['user']

user = Blueprint('user', __name__)
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'user.login'
login_manager.login_message = None

core = Blueprint('core', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first()


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('user.login'))


@core.route("/")
@core.route("/user/login/", methods=["GET", "POST"])
@validate_form(LoginForm)
def login():
    form = g.form
    condition = Q(user_name=trim(form.user_name.data))
    user = User.objects.filter(condition).first()
    if user is None:
        return fail_jsonify(code=codes.NOT_USER)

    if not user.check_password(trim(form.password.data)):
        return fail_jsonify(code=codes.WRONG_PASSWORD)

    if not (user.is_authenticated() and user.is_active()):
        return fail_jsonify(code=codes.UNAUTHENTICATED)

    remember_me = True if form.remember_me.data else False
    login_user(user, remember=remember_me)
    User.objects(id=user.id).update_one(last_login=datetime.utcnow())

    res = jsonify(code=0)
    res.set_cookie('token', get_token())
    return res


@core.route('/user/logout/', methods=["GET"])
@login_required
def logout():
    user_name = current_user.user_name
    logout_user()
    session.clear()

    current_app.logger.info('User %s logout' % user_name)

    res = jsonify(code=0)
    res.set_cookie('token', '', expires=0)
    return res


@core.route('/user/change_password/', methods=['POST'])
@login_required
@validate_form(ResetPasswordForm)
def change_password():
    form = g.form

    user = User.objects.filter(id=current_user.id).first()
    if user is None:
        return fail_jsonify(code=codes.NOT_USER)

    if not user.check_password(form.old_password.data):
        return fail_jsonify(code=codes.WRONG_PASSWORD)

    user.change_password(form.new_password.data)
    user.save()
    return ok_jsonify({})


@core.route('/user/edit/', methods=['POST'])
@login_required
def edit_userinfo():
    pass


@core.route('/user/info/')
@login_required
def user_info():
    user_info = User.objects.filter(id=current_user.id).first()
    if user_info is None:
        return fail_jsonify(code=codes.NOT_USER)

    return ok_jsonify(data=dict(user_info=user_info))


@core.route('/user/register/', methods=['POST'])
@validate_form(RegisterForm)
def register():
    form = g.form
    condition = Q(user_name=form.user_name.data)
    if User.objects.filter(condition).first():
        return fail_jsonify(code=codes.USER_EXISTED)

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

    return ok_jsonify(data=dict(user=user))
