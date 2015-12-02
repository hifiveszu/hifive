#! -*- coding: utf-8 -*-

import logging
import os


class BaseConfig(object):
    DEBUG = False

    CACHE_TYPE = 'redis'
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_KEY_PREFIX = 'hifive:'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0

    MONGODB_SETTINGS = dict(
        host='127.0.0.1',
        port=27017,
        db='hifive'
    )


class DevelopmentConfig(BaseConfig):
    DEBUG = True

    LOG_LEVEL_NAME = logging.DEBUG


class TestingConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


config = {
    'development': 'admin.config.DevelopmentConfig',
    'production': 'admin.config.ProductionConfig',
    'default': 'admin.config.DevelopmentConfig',
    'testing': 'admin.config.TestingConfig'
}


def configure_app(app):
    config_name = os.getenv('FLASK', 'default')
    app.config.from_object(config[config_name])

    # 可以把 etc/server.example.conf 复制一份到 admin/server.conf
    # 然后修改相应的配置项。admin/server.conf 没有添加到版本库，所以不会出现冲突
    app.config.from_pyfile('server.conf', silent=True)
