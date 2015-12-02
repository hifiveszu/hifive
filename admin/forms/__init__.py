#! -*- coding: utf-8 -*-
import datetime

from wtforms import Form
from wtforms.fields import DateField, DateTimeField, IntegerField
from wtforms.validators import ValidationError

from app.utils import valid_object_id


class JsonSerializableForm(Form):
    def to_dict(self, exclude_keys=()):
        result = {}
        for field in self:
            if field.name in exclude_keys:
                continue

            if isinstance(file, (DateField, DateTimeField)):
                value = field._value()
            else:
                value = field.data

            result[field.name] = value
        return result

    def purify(self):
        return dict((k, v) for k, v in self.to_dict().iteritems() if v)


class ObjectIdType(object):
    def __init__(self, message=None, allow_blank=False):
        self.message = message
        if self.message is None:
            self.message = "Is not a valid ObjectId"
        self.allow_blank = allow_blank

    def __call__(self, form, field):
        if not field.data and self.allow_blank:
            return
        if not valid_object_id(field.data):
            raise ValidationError(self.message)


class PageForm(Form):
    pageIndex = IntegerField(default=1)
    pageSize = IntegerField(default=10)

    @property
    def skip(self):
        return (self.pageIndex.data - 1) * self.pageSize.data

    @property
    def limit(self):
        return self.pageSize.data
