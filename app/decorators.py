#!/usr/bin/env python
# -*- coding=utf-8 -*-
import functools

from flask import request, g
from app.utils.api_utils import api_error


def validate_form(form_class):
    def decorator(view_func):
        @functools.wraps(view_func)
        def inner(*args, **kwargs):
            if request.method == "GET":
                formdata = request.args
            else:
                formdata = request.form if request.form else request.json

            form = form_class(form_data)
            if not form.validate():
                return api_error

        return inner

    return decorator
