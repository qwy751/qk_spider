# -*- coding: utf-8 -*-

import sys

sys.path.append('..')

from unittest import TestCase

from app.datasource.cup.cup import ChinaUnionPay


class TestChinaUnionPay(TestCase):
    def test_get_data(self):
        cup = ChinaUnionPay()
        result = cup.query(user_name_cn=u'谭俊峰',
                           mobile_num='18192349450',
                           personal_id='430102197111062010',
                           card_id='4340624220484768')
        print(result)
        assert result


if __name__ == '__main__':
    tcup = TestChinaUnionPay()
