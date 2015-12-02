#! -*- coding: utf-8 -*-

import datetime
import functools
import time


def isoformat(dt, fmt=None):
    """ Format datetime.datetime date to ISO8601 Format
    """
    if not fmt:
        if isinstance(dt, datetime.datetime):
            fmt = '%Y-%m-%dT%H:%M:%SZ'
        elif isinstance(dt, datetime.date):
            fmt = '%Y-%m-%d'
        return dt.strftime(fmt)
    return None


def str_to_datetime(str, fmt='%Y-%m-%d %H:%M:%S'):
    return datetime.datetime.strptime(str, fmt)


def utcnow():
    return datetime.datetime.utcnow()


def date_to_datetime(dt):
    if isinstance(dt, datetime.datetime):
        return dt
    return datetime.datetime.combine(dt, datetime.time(0, 0, 0))


def utc_to_beijing(dt):
    return dt - datetime.timedelta(hours=8)


def timeit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        rv = func(*args, **kwargs)
        taken = (time.time() - start) * 1000
        print '%s taken %s ms' % (func.__name__, taken)
        return rv

    return wrapper
