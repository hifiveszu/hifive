#! -*- coding: utf-8 -*-
import datetime

from mongoengine import (
    StringField, BooleanField,
    DateTimeField, SequenceField
)

from app.models import BaseDocument


class Activity(BaseDocument):
    id = SequenceField(primary_key=True)
    type = StringField()
    name = StringField(max_length=50, required=True)
    name_en = StringField(max_length=50)
    is_hot = BooleanField(default=False)
    last_modified = DateTimeField(default=datetime.datetime.utcnow)
    date_added = DateTimeField(default=datetime.datetime.utcnow)
    is_active = BooleanField(default=True)
