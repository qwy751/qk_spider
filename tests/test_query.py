# -*- coding: utf-8 -*-
from unittest import TestCase
import pydevd
# pydevd.settrace('licho.iok.la', port=44957, stdoutToServer=True, stderrToServer=True)

import sys
from app import db, create_app

sys.path.append('..')

from app.datasource.query import Query


class TestQuery(TestCase):
    query = Query()

    def setUp(self):
        self.app = create_app('development')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        pass

    def test_query(self):
        self.query.query(user_name_cn=u'孙立超',
                         mobile_num='15829551989',
                         personal_id='210114198701251232',
                         card_id='610527199005154925')

if __name__ == '__main__':
    tq = TestQuery()
    tq.test_query()
