#! -*- coding: utf-8 -*-
import re

from wtforms import Form
from wtforms.fields import DateField, DateTimeField
from wtforms.validators import ValidationError, Regexp

from app.utils import valid_object_id


class JsonSerializableForm(Form):
    def as_dict(self, exclude={}):
        result = {}
        for field in self:
            if field.name in exclude:
                continue

            if isinstance(field, (DateField, DateTimeField)):
                value = field._value()
            else:
                value = field.data

            result[field.name] = value

        return result

    def purify(self):
        return dict((k, v) for k, v in self.as_dict().iteritems() if v)


class ObjectIdType(object):
    def __init__(self, message=None, allow_blank=False):
        self.message = message

        if self.message is None:
            self.message = "Not a valid id"

        self.allow_black = allow_blank

    def __call__(self, form, field):
        if not field.data and self.allow_black:
            return

        if not valid_object_id(field.data):
            raise ValidationError(self.message)


class ChineseMobileNo(Regexp):
    def __init__(self, message='Invalid mobile phone number'):
        regex = r'^1[0-9]{10}$|^86[0-9]{11}$|^852[0-9]{8}$|^853[0-9]{8}$|^886[0-9]{9}$'
        super(ChineseMobileNo, self).__init__(regex, re.IGNORECASE, message)
