# -*- coding=utf-8 -*-
"""
    TDD
    Usage: nosetests example_unit_test.py
"""
import unittest
import requests

from app import create_app


class TDDTestUserOperation(unittest.TestCase):
    def setUp(self):
        self.db_name = 'test_hifive'

        MONGODB_SETTING = dict(
            db=self.db_name,
            alias="default",
            host="127.0.0.1",
            port=27017,
        )
        test_config = dict(
            MONGODB_SETTING=MONGODB_SETTING,
            WTF_CSRF_ENABLED=False,
            MONGO_HOST="127.0.0.1",
            MONDO_POST=27017,
            MONGO_DBNAME='test_hifive',
            TESTING=True,
        )
        app = create_app(config_name=test_config)
        self.app = app
        self.test_client = app.test_client()

    def test_register(self):
        pass

    def test_login(self):
        pass

    def test_logout(self):
        pass

    def test_edit_user_info(self):
        pass

    def test_change_password(self):
        pass


if __name__ == "__main__":
    unnittest.main()
