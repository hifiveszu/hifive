#!/usr/bin/env python
# -*- coding=utf-8 -*-
import functools

from flask import request, g
from werkzeug.utils import MultiDict

from app.utils.api_utils import api_error


def validate_form(form_class):
    def decorator(view_func):
        @functools.wraps(view_func)
        def inner(*args, **kwargs):
            if request.method == "GET":
                formdata = request.args
            else:
                formdata = request.form if request.form else \
                    MultiDict(request.json(force=True))

            form = form_class(formdata)
            if not form.validate():
                return api_error(10013)
            g.form = form

        return inner

    return decorator
