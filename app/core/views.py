# -*- coding=utf-8 -*-
from datetime import datetime

from flask import Blueprint, jsonify, redirect, \
    request, url_for, session
from flask.ext.login import current_user, current_app, \
    logout_user, login_user, login_required, LoginManager
from werkzeug.datastructures import MultiDict

from app.core.models import User
from app.core.forms import LoginForm, ResetPasswordForm, RegisterForm
from app.utils.common_utils import trim
from app.utils.core_utils import get_token
from app.utils.api_utils import api_ok, api_error

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
def login():
    if request.form:
        args = request.form
    else:
        args = MultiDict(request.get_json(force=True))

    form = LoginForm(args)
    if not form.validate():
        return api_error(10000, msg=dict(msg=form.errors))

    user = User.objects.filter(user_name=trim(form.user_name.data)).first()
    if user is None:
        return api_error(10001)

    if not user.check_password(trim(form.password.data)):
        return api_error(10002)

    if not (user.is_authenticated() and user.is_active()):
        return api_error(10003)

    remember_me = True if args.get('remember_me', '') else False
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
def change_password():
    if request.form:
        args = request.form
    else:
        args = MultiDict(request.get_json(force=True))

    if not args.get('old_password'):
        return api_error(10004)

    form = ResetPasswordForm(formdata=args)
    if form.validate():
        user = User.objects.filter(id=current_user.id).first()
        if user is None:
            return api_error(10005)

        if not user.check_password(args.get('old_password')):
            return api_error(10006)

        user.change_password(args.get('new_password'))
        user.save()
        return jsonify(success=True)

    else:
        errors = {}
        for key, value in form.errors.iteritems():
            errors[getattr(form, key).label.text] = value[0]

        return api_error(10007, msg=errors.items())


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
def register():
    if request.form:
        args = request.form
    else:
        args = MultiDict(request.get_json(force=True))

    form = RegisterForm(args)
    if form.validate():
        if User.objects.filter(user_name=form.user_name.data).first():
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
        try:
            user = User.objects.create(**obj)
            user.change_password(form.password.data)
            user.save()
            return api_ok(data=dict(user=user))
        except Exception as e:
            return api_error(10010, msg=str(e))
    else:
        errors = {}
        for key, value in form.errors.iteritems():
            errors[getattr(form, key).label.text] = value[0]

        return api_error(10011, msg=errors.items())
