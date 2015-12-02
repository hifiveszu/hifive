#! -*- coding=utf-8 -*-

from flask import Flask
from werkzeug.routing import BaseConverter
from werkzeug.contrib.fixers import ProxyFix

from .config import configure_app
from app.models import db, cache


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


def create_app():
    app = Flask(__name__)

    app.wsgi_app = ProxyFix(app.wsgi_app)

    app.url_map.converters['regex'] = RegexConverter
    configure_app(app)

    # add config
    return app


def register_routes(app):
    from admin.views.activity import admin_activity

    app.register_blueprint(admin_activity, url_prefix='/hifiveadmin')


def setuo_database(app):
    db.init_app(app)
    cache.init_app(app)
