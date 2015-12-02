#! -*- coding: utf-8 -*-

__author__ = 'KittoZheng'

import functools

from flask import current_app as app
from flask import g, jsonify, request
from werkzeug.datastructures import MultiDict

from admin.utils import codes


def ok_jsonify(data):
    return jsonify(
        code=0,
        data=data,
    )


def fail_jsonify(code, msg, detail=''):
    return jsonify(
        code=code,
        error=dict(
            msg=msg,
            detail=detail
        )
    )


def validate_form(form_class):
    def wrapper(view_func):

        @functools.wraps(view_func)
        def validate(*args, **kwargs):
            if request.method == 'GET':
                formdata = request.args
            else:
                if request.json:
                    formdata = MultiDict(request.json)
                else:
                    formdata = request.form

            form = form_class(formdata)
            if not form.validate():
                print form.data
                app.logger.info('invalid args, error: %s, args: %s',
                                form.errors, formdata)
                return fail_jsonify(
                    code=codes.FORM_VALIDATION_ERROR,
                    msg=u'表单校验错误',
                    detail=form.errors
                )

            g.form = form
            return view_func(*args, **kwargs)

        return validate

    return wrapper


def retry_on_server_error(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        have_tried = 0
        max_try_times = 5
        while have_tried < max_try_times:
            try:
                resp = func(*args, **kwargs)
            except Exception as e:
                print e
                have_tried += 1
                app.logger.warn('Retry func %s, have tried: [%s], remained: [%d]',
                                func.__name__, have_tried, max_try_times - have_tried)
                continue

            if resp is None or not (500 <= resp.status_code <= 599):
                return resp
            app.logger.warn('Retry func %s, have tried: [%s], remained: [%d]',
                            func.__name__, have_tried, max_try_times - have_tried)
            have_tried += 1

    return decorator
