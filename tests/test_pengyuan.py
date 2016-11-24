# -*- coding: utf-8 -*-

import sys
from unittest import mock

sys.path.append('../')
import pydevd
# pydevd.settrace('heqiang.imwork.net', port=44957, stdoutToServer=True, stderrToServer=True)

from unittest import TestCase
import xmltodict
import json
from lxml import etree
import os

import queue
import sys
sys.path.append('../')
from app.datasource.pengyuan.pengyuan import PengYuan, FORMAT
from app.datasource.pengyuan.transform import *

class TestPengYuan(TestCase):

    def test_create_query_condition_xml(self, name='sunlc',
                                    # documentNo='2101141098701251234',
                                    # accountNo='637933021912',
                                    # openBankNo='1001',
                                    # mobile='168234214123',
                                    # subreportIDs='1234',
                                    # queryReasonID='fuck',
                                    refID=None):
        py = PengYuan()
        result = py.create_query_condition("123")
        assert result=='<conditions><condition queryType="123"><item><name>name</name><value>sunlc</value></item></condition></conditions>'

    def test_create_query_condition_json(self, name='sunlc'):
        py = PengYuan()
        result = py.create_query_condition('123', query_type=FORMAT.JSON)
        print(result)

    def test_create_query_condition(self):
        mock

    def test_query_personal_id_risk(self):
        sub_report = {10604: True, 10603: False, 14200: True}
        query_reason = {101: u"货款审批",
                        102: u"货款贷后管理",
                        103: u"贷款催收",
                        104: u"审核担保人信用",
                        105: u"担保/融资审批",
                        202: u"信用卡货后管理",
                        201: u"信用卡审批",
                        203: u"信用卡催收",
                        301: u"加强税源基础管理",
                        302: u"追缴欠税",
                        303: u"商户信用",
                        304: u"申报创新人才奖",
                        305: u"失业人员小额贷款担保审批",
                        306: u"深圳市外来务工人员积分入户申请",
                        401: u"车货保证保险审批",
                        402: u"审核国货保证保险担保人信用",
                        501: u"求职",
                        502: u"招聘",
                        503: u"异议处理",
                        901: u"了解个人信用",
                        999: u"其他"
                        }
        sr = '10604'
        qr = '101'
        py = PengYuan()
        result = py.query_personal_id_risk(name=u'孙立超',
                                           documentNo='210114198701251232',
                                           subreportIDs='10604',
                                            queryReasonID='101')

        print(result)

    def test_query_airplane_info(self):
        py = PengYuan()
        result = py.query_airplane_info(name=u'李大林', documentNo='511225198001093698')
        print(result)

    def test_query_card_pay_record(self):
        py = PengYuan()
        result = py.query_card_pay_record(name=u'谭俊峰', cardNos='4340624220484768')
        print(result)

    def test_query_career_capacity(self):
        py = PengYuan()
        result = py.query_career_capacity(name=u'张含', documentNo='360521840524002')
        print(result)

    def test_query_personal_enterprise_telephone(self):
        py = PengYuan()
        result = py.query_personal_enterprise_telephone(tel='031166005777')
        print(result)

    def test_query_personal_revenue_assess(self):
        py = PengYuan()
        result = py.query_personal_revenue_assess(name=u'谭俊峰', documentNo='4340624220484768',
                                                  corpName=u'乾康(上海)金融信息服务股份有限公司')

    def test_query_personal_bank_info(self):
        py = PengYuan()
        result = py.query_personal_bank_info(name=u'谭俊峰', documentNo='430102197111062010',
                                             mobile='18192349450', accountNo='4340624220484768')
        print(result)

    def test_query_open_bank_info(self):
        py = PengYuan()
        result = py.query_open_bank_info(accountNo='4340624220484768')
        print(result)

    def test_query_enterprise_last_one_year(self):
        py = PengYuan()
        result = py.query_enterprise_last_one_year(corpName=u'鹏元征信有限公司')
        print(result)

    def test_query_personal_last_two_years_info(self):
        py = PengYuan()
        result = py.query_personal_last_two_years_info(name=u'谭俊峰', documentNo='430102197111062010')
        print(result)

    def test_query_enterprise_operation(self):
        py = PengYuan()
        result = py.query_enterprise_operation(corpName=u'温州市工业品商贸公司')

    def test_query_trade_company_reprot(self):
        py = PengYuan()
        result = py.query_trade_company_reprot(corpName=u'北京京崇博五金工具有限公司')

    def test_query_car_info(self):
        py = PengYuan()
        result = py.query_car_info(name=u'谭俊峰', documentNo='430102197111062010',
                                   licenseNo='陕AKQ615', carType='02')
        print(result)

    def test_query_enterprise_info(self):
        py = PengYuan()
        result = py.query_enterprise_info(corpName=u'北京京崇博五金工具有限公司')
        print(result)

    def test_query_mini_loan_rish_grade(self):
        py = PengYuan()
        result = py.query_mini_loan_rish_grade(name=u'谭俊峰', documentNo='430102197111062010',
                                               province=u'陕西', city=u'西安',
                                               corpName=u'乾康(上海)金融信息服务股份有限公司', positionName=u'经理')
        print(result)

    def test_query(self):
        py = PengYuan()
        result = py.query(user_name_cn=u'谭俊峰',
                          mobile_num='18192349450',
                          personal_id='430102197111062010',
                          card_id='4340624220484768',
                          py_open_bank_id='4340624220484768',
                          license_no='430102197111062010')
        print(result)


if __name__ == '__main__':
    tpy = TestPengYuan()
    result = queue.Queue()
    # tpy.test_query()
    tpy.test_query_airplane_info()
    tpy.test_query_card_pay_record()
    tpy.test_query_career_capacity()
    tpy.test_query_personal_enterprise_telephone()
    tpy.test_query_personal_revenue_assess()
    tpy.test_query_personal_bank_info()
    tpy.test_query_open_bank_info()
    tpy.test_query_enterprise_last_one_year()
    tpy.test_query_personal_last_two_years_info()
    tpy.test_query_car_info()
    tpy.test_query_enterprise_operation()
    tpy.test_query_trade_company_reprot()
    tpy.test_query_enterprise_info()
    tpy.test_query_mini_loan_rish_grade()