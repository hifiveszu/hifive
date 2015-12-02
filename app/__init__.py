#! -*- coding: utf-8 -*-
import logging
import os
import requests

from flask import Flask, request
from flask_login import LoginManager
from flask.ext.mongoengine import MongoEngine
from flask.ext.pymongo import PyMongo
from werkzeug.contrib.fixers import ProxyFix

from app.config import configure_app
from app.views.core import login_manager

mongo_engine = MongoEngine()
pymongo = PyMongo()


def create_app(config_name):
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    configure_app(app, config_name)

    login_manager.init_app(app)
    mongo_engine.init_app(app)
    pymongo.init_app(app)
    register_routes(app)
    register_babel(app)

    return app


def register_routes(app):
    from app.views.core import core
    from app.views.api import api

    app.register_blueprint(core, url_prefix="/hifive")
    app.register_blueprint(api, url_prefix="/hifive")


def register_babel(app):
    """Configure Babel for internationality."""
    from flask_babel import Babel

    babel = Babel(app)
    supported = app.config.get('BABEL_SUPPORTED_LOCALES', ['en', 'zh'])
    default = app.config.get('BABEL_DEFAULT_LOCALE', 'en')

    @babel.localeselector
    def get_locale():
        return request.accept_languages.best_match(supported, default)


def register_logger(app):
    """Track the logger for production mode."""
    if app.debug:
        return

    # 按时间切分日志, 默认以小时分
    from logging.handlers import TimedRotatingFileHandler

    log_path = app.config.get('LOG_PATH')
    try:
        if not os.path.exists(log_path):
            os.makedirs(log_path)
    except TypeError, e:
        print e
        return

    filename = os.path.join(log_path, 'hifive.log')

    handler = TimedRotatingFileHandler(filename)
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter('[%(asctime)s] %(levelname)-8s %(name)s: %(message)s')
    handler.setFormatter(formatter)

    app.logger.addHandler(handler)


# def config_errcode(app):
#     try:
#         resp = requests.get(app.config['ERRCODE_HOST'])
#         app.config['errcode'] = resp.json()
#     except Exception as e:
#         raise Exception("Get error code failed, reason: %s" % e)
