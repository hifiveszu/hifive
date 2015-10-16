# -*- coding=utf-8 -*-
from flask import jsonify, current_app

def api_ok(data=None):
    return jsonify({
        'code': 0,
        'data': data or {}
    })


def api_error(code=1, msg=''):
    error = {}
    if msg is not None:
        error = dict(msg=msg)
    else:
        error = current_app.config['ERRORS'].get(
            str(code), {"msg": u'服务器错误'}
        )

    return jsonify({
        'code': code,
        'error': error
    })

