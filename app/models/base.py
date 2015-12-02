#! -*- coding: utf-8 -*-
import datetime
from bson import ObjectId

from mongoengine import Document
from flask_cache import Cache
from flask_mongoengine import MongoEngine

from app.utils import isoformat

cache = Cache()
db = MongoEngine

class BaseDocument(Document):
    meta = {
        'abstarct': True,
        'allow_inheritance': True
    }

    def to_dict(self, exclude=set(), only=set()):
        """ Convert Model instance to dict

        :param exclude: exclude fields
        :param only: only fields
        :return: dict
        """
        rv = {}
        fields = set(self._fields.keys())
        if only:
            fields &= set(only)
        elif exclude:
            fields -= set(exclude)
        for field in fields:
            value = getattr(self, field)
            if isinstance(value, (datetime.datetime, datetime.date)):
                value = isoformat(value)
            elif isinstance(value, ObjectId):
                value = str(value)
            rv[field] = value
        return rv

    @classmethod
    def find_one(cls, **kwargs):
        return cls.objects(**kwargs).first()

    @classmethod
    def get(cls, pk, cacheable=False, timeout=3600):
        if cacheable:
            key = '%s:%s' % (cls.__name__.lower(), pk)
            value = cache.get(key)
            if value:
                return value
        value = cls.find_one(pk=pk)
        if cacheable and value:
            cache.set(key, value, timeout)
        return value

    @classmethod
    def get_or_create(cls, **kwargs):
        lookup = kwargs.copy()
        defaults = kwargs.pop('defaults', {})
        obj = cls.find_one(**lookup)
        if not obj:
            params = dict([(k, v) for k, v in kwargs.items()])
            params.update(defaults)
            obj = cls(**params)
            obj.save()
            return obj, True
        return obj, False
