# -*- coding=utf-8 -*-
import datetime

from flask import current_app, request
from flask.ext.login import current_user


def get_token(user_id=None):
    from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

    expiration = int(current_app.permanent_session_lifetime.total_seconds())
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)

    if user_id is None:
        token = s.dumps({'token': str(current_user.id)})
    else:
        token = s.dumps({'token': str(user_id)})

    return token





