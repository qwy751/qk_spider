# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import pydevd
pydevd.settrace('licho.iok.la', port=44957, stdoutToServer=True, stderrToServer=True)

import json
from base64 import b64encode
from unittest import TestCase
import requests
from flask import url_for

from app import create_app, db
from app.api_1_0 import api
from app.consts import APPLICATION_JSON
from app.models import Role, User


class TestDataSources(TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_api_headers(self, username, password):
        return{
            'Authorization': 'Basic' + b64encode((username + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept': APPLICATION_JSON,
            'Content-Type': APPLICATION_JSON
        }

    def test_token_auth(self):
        r = Role.query.filter_by(name='User').first()
        self.assertIsNotNone(r)
        u = User(email='sunlc@qkjr.com.cn', password='cat', confirmed=True, role=r)
        db.session.add(u)
        db.session.commit()
        pass

    def test_get(self):
        params = {
            'user_name_cn': u'阎伟晨',
            'mobile_num': '15829551989',
            'personal_id': '610102199407201510',
            'card_id': '610527199005154925'
        }
        url = url_for('api.data')
        response = self.client.get(url_for('api.data'), query_string=params, content_type=APPLICATION_JSON)
        self.assertTrue(response.status_code == 200)

if __name__ == '__main__':
    tds = TestDataSources()
    tds.setUp()
    tds.test_get()
    tds.tearDown()
