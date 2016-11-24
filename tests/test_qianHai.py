import json
from unittest import TestCase


# -*- coding: utf-8 -*-
from app.datasource.qianhai.dataSecurityUtil import DataSecurityUtil
from app.datasource.qianhai.qianhai import QianHai


class TestQianHai(TestCase):

    url = 'https://test-qhzx.pingan.com.cn:5443/do/dmz/query/credoo/v1/MSC8005'
    # url = 'https://test-qhzx.pingan.com.cn:5443/do/dmz/query/blacklist/v1/MSC8004'
    kwargs = {
        'batchNo': '29342fasdf',
        'personal_id': '430102197111062010',
        'user_name_cn': u'谭俊峰',
        'mobile_num': '18192349450',
        'card_id': '4340624220484768',
        'email': 'sunlc@qkjr.com.cn',
        'weibo_id': 'chinabhsun',
        'wechat_id': 'leecho_sun',
        'qq_id': '314509438',
        'taobao_id': 'chinabhsun',
        'jd_id': 'leechor_sun',
        'amazon_id': 'chinabhsun',
        'yhd_id': '',
        'auth_code': 'asdfasdhfh3',
        'auth_date': '2016-11-22 15:28:01',
        'seq_no': 'adfj'
    }

    def test_format_json_encBusData(self):
        qh = QianHai()
        result = qh.format_json_enc_busi_data(**TestQianHai.kwargs)
        print(result)

    def test_format_json_securityInfo(self):
        qh = QianHai()
        result = qh.format_json_security_info('fasdfasdfas')
        print(result)

    def test_send_json_with_https(self):
        header = QianHai.format_json_header()
        enc_busi_data = QianHai.format_json_enc_busi_data(**TestQianHai.kwargs)
        busi_data = QianHai.format_json_busi_data(enc_busi_data)
        security_info = QianHai.format_json_security_info(enc_busi_data)

        message = '{' + header + ',' + busi_data + ',' + security_info + '}'

        result = QianHai.send_json_with_https(surl=TestQianHai.url, json_str=message)
        js = json.loads(result.text)
        busi_data_result = js.get('busiData')
        security_info_result = js.get('securityInfo').get('signatureValue')
        v = DataSecurityUtil.verify_data(busi_data_result.encode(), security_info_result)
        final_result = DataSecurityUtil.decrypt(busi_data_result, QianHai.check_sum).decode('utf-8', 'ignore')
        print(final_result)


