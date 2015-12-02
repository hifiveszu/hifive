# -*- coding: utf-8 -*-

from .common_utils import trim, valid_object_id
from .core_utils import get_token
from .time_utils import isoformat
import codes

from flask import jsonify


def ok_jsonify(data):
    return jsonify(code=0, data=data)


def fail_jsonify(code, message):
    return jsonify(code=code, message=message)
