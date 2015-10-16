#!/usr/bin/env python
# -*- coding=utf-8 -*-

import bson
import datetime

from flask import request
from flask.ext.login import UserMixin, current_user, current_app
from mongoengine import StringField, EmailField, BooleanField, \
    DateTimeField, ObjectIdField, Document, signals
from werkzeug import security
from werkzeug.local import LocalProxy

__all__ = ['User', 'OperationLog']


def get_current_user_id():
    if current_user and not current_user.is_anonymous():
        return current_user.id
    return None


class User(Document, UserMixin):
    id = ObjectIdField(primary_key=True, default=lambda: bson.ObjectId())
    user_name = StringField(verbose_name=u'用户名', max_length=50, required=True, unique=True)
    password = StringField(verbose_name=u'密码', max_length=200, required=True)
    email = EmailField(verbose_name=u'邮箱', max_length=50, required=True)
    phone = StringField(verbose_name=u'手机号码', max_length=50)
    avatar = StringField(verbose_name=u'头像', max_length=255)
    hasher = StringField(verbose_name=u'加密类型', max_length=200)
    salt = StringField(verbose_name=u'加密盐', max_length=200)
    active = BooleanField(verbose_name=u'用户状态', default=True)
    is_superuser = BooleanField(verbose_name=u'超级用户', default=False, required=True)
    is_manager = BooleanField(verbose_name=u'管理员', default=False, required=True)
    is_staff = BooleanField(verbose_name=u'内部员工', default=False, required=True)
    is_banned = BooleanField(verbose_name=u'是否在黑名单', default=False)
    first_name = StringField(verbose_name=u'名字', max_length=20, required=True)
    last_name = StringField(verbose_name=u'姓氏', max_length=20, required=True)
    full_name = StringField(verbose_name=u'全名', max_length=40, required=True)
    last_login = DateTimeField(verbose_name=u'最近登录时间', default=datetime.datetime.utcnow)
    created_at = DateTimeField(verbose_name=u'创建时间', default=datetime.datetime.utcnow)
    updated_at = DateTimeField(verbose_name=u'更新时间', default=datetime.datetime.utcnow)

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    @staticmethod
    def create_token(length=16):
        return security.gen_salt(length)

    @staticmethod
    def create_password(self, password="hifive4u"):
        return security.generate_password_hash(self.password, password)

    def check_password(self, password):
        return security.check_password_hash(self.password, password)

    def change_password(self, password):
        return self.create_password(password)

    @classmethod
    def post_save(cls, sender, document, **kwargs):
        identity = get_user_identity(document)
        action_log = "%s%s%s" + unicode(identity) + "%s"
        post_save_log(document.user_name, action_log, **kwargs)

    @classmethod
    def post_delete(cls, sender, document, **kwargs):
        identity = get_user_identity(document)
        action_log = "%s%s%s" + unicode(identity) + "%s"
        post_delete_log(document.user_name, action_log, **kwargs)


    def __repr__(self):
        return '<User %r>' % (self.user_name)

    def __unicode__(self):
        return self.user_name

signals.post_save.connect(User.post_save, sender=User)
signals.post_delete.connect(User.post_delete, sender=User)


class OperationLog(Document):
    operator = StringField(max_length=50)
    operator_id = ObjectIdField(verbose_name=u"操作人Id")
    operator_ip = StringField(max_length=20)
    action = StringField(max_length=25)
    action_log = StringField(max_length=255)
    created_at = DateTimeField(verbose_name=u'创建时间', default=datetime.datetime.utcnow)


def get_user_identity(user):
    if not isinstance(user, User) \
            and not isinstance(user, LocalProxy):
        return u"测试"

    if user.is_superuser:
        return u"超级管理员"
    elif user.is_manager:
        return u"系统管理员"
    else:
        return u"用户"


def post_save_log(document_name, action_log, **kwargs):
    if 'created' in kwargs and current_app:
        operator_id = None
        if current_user and not current_user.is_anonymous:
            operator = current_user.user_name
            operator_id = current_user.id
            identity = get_user_identity(current_user)
        else:
            operator = "shell"
            identity = u"测试"

        operation = u"新增" if kwargs['created'] else u"修改"
        log = action_log % (identity, operator, operation, document_name)

        current_app.logger.info(log)

        if operator_id:
            if request and request.remote_addr:
                operator_ip = request.remote_addr
            else:
                operator_ip = "127.0.0.1"

            OperationLog.objects.create(
                operator=current_user.user_name,
                operator_id=operator_id,
                operator_ip=operator_ip,
                action=operation,
                action_log=log,
                created_at=datetime.datetime.utcnow()
            )


def post_delete_log(document_name, action_log, **kwargs):
    if current_app:
        operator_id = None
        if current_user and not current_user.is_anonymous:
            operator = current_user.user_name
            operator_id = current_user.id
            identity = get_user_identity(current_user)
        else:
            operator = "shell"
            identity = u"测试"

        operation = u"删除"
        log = action_log % (identity, operator, operation, document_name)
        current_app.logger.info(log)

        if operator_id:
            if request and request.remote_addr:
                operator_ip = request.remote_addr
            else:
                operator_ip = "127.0.0.1"

            OperationLog.objects.create(
                operator=current_user.user_name,
                operator_id=operator_id,
                operator_ip=operator_ip,
                action=operation,
                action_log=log,
                created_at=datetime.datetime.utcnow()
            )
