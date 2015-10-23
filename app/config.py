# -*- coding=utf-8 -*-
from datetime import timedelta
import os


class BaseConfig(object):
    SECRET_KEY = os.environ.get(
        'secret_key', '24dbb12803ad9f2dadd3dd6cf6156f3301294e91a8d94f05'
    )

    REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
    REDIS_PORT = os.environ.get('REDIS_PORT', 6379)

    SESSION_COOKIE_NAME = 'hifive_session'
    PERMANENT_SESSION_LIFETIME = timedelta(days=2)

    #: i18n settings
    BABEL_DEFAULT_LOCALE = "zh"
    BABEL_SUPPORTED_LOCALES = ["zh"]

    # password settings
    PASSWORD_SECRET = "hifivepwdsecret"
    DEFAULT_PASSWORD = "111111"

    # mongo settings
    MONGODB_SETTINGS = {
        "db": "hifive",
        "alias": "default",
        "host": "127.0.0.1",
        "port": 27017,
    }
    MONGO_HOST = "127.0.0.1"
    MONGO_PORT = 27017
    MONGO_DBNAME = "hifive"


    # log settings
    LOG_PATH = "/var/log/hifive/"

    # csrf_token expired time
    WTF_CSRF_TIME_LIMIT = 3600 * 24
    CSRF_ENABLED = False
    WTF_CSRF_ENABLED = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


config = {
    "development": "app.config.DevelopmentConfig",
    "production": "app.config.ProductionConfig",
    "default": "app.config.DevelopmentConfig",
    'testing': 'app.config.TestingConfig'
}


def configure_app(app, config_name):
    app.config.from_object(config[config_name])

    # 可以把 etc/server.example.conf 复制一份到 app/local.conf
    # 然后修改相应的配置项。app/local.conf 没有添加到版本库，所以不会出现冲突
    app.config.from_pyfile('local.conf', silent=True)
    app.config.from_pyfile('error_code.py', silent=True)

