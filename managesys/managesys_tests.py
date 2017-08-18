# -*- coding:utf-8 -*-  
"""
@version: ??
@author: zhayufeng
@describe:
@contact: zyfjfj@163.com
@software: PyCharm
@file: test
@time: 2017/8/16 9:36
"""
import os
import unittest
import tempfile

from flask import request

from managesys import app
from managesys.model.models import User
from managesys.model.work_flow_models import UserWorkflowInfo


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
    def test_user(self):
        rv = self.app.get('/')
        print(User.query.all())
        assert   rv.data

    def login(self, email, password):
        return self.app.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def test_login_logout(self):
        rv = self.login('admin', 'default')
        assert b'You were logged in' in rv.data
        assert b'You were logged out' in rv.data
        rv = self.login('adminx', 'default')
        assert b'Invalid username' in rv.data
        rv = self.login('admin', 'defaultx')
        assert b'Invalid password' in rv.data
if __name__ == '__main__':
    unittest.main()
