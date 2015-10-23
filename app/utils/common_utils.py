# -*- coding=utf-8 -*-
from bson import objectid


def trim(s):
    return s.strip(' \t\n\r') if s else ''


def valid_object_id(id):
    if not id:
        return False

    try:
        _ = objectid.ObjectId(id)
    except (objectid.InvalidId, TypeError):
        return False
    else:
        return True
