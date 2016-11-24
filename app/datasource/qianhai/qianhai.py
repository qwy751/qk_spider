import base64
import json
import random
import string
import sys
import os
from datetime import datetime

import requests
from pathlib import Path

from app.datasource.qianhai.dataSecurityUtil import DataSecurityUtil
from app.datasource.third import Third
from app.datasource.zzc.tranform import format_result
from ..utils.tools import params_to_dict, SafeSub
from ..configuration import config


class QianHai(Third):
    """
    钱海的查询接口
    """
    qh_config = config.get('qianhai')
    url = qh_config.get('url')
    user_name = qh_config.get('userName')
    user_password = qh_config.get('userPassword')
    net_type = qh_config.get('netType')
    trans_name = qh_config.get('transName')
    product_id = qh_config.get('productId')
    api_version = qh_config.get('apiVer')
    org_code = qh_config.get('orgCode')
    chnl_id = qh_config.get('chnlId')
    auth_code = qh_config.get('authCode')
    check_sum = qh_config.get('checkSum')
    source = 'qianhai'

    headers = {'Content-Type': 'application/json; charset=utf8'}

    def query(self):
        pass

    @staticmethod
    def format_json_header():
        trans_no = datetime.now().strftime('%Y%m%d%S') + \
                  ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(14))
        trans_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        header = r'"header":{{' \
                 r'"orgCode": "{orgCode}", ' \
                 r'"chnlId": "{chnlId}",' \
                 r'"transNo": "{trans_no}",' \
                 r'"transDate": "{trans_date}",' \
                 r'"authCode": "{authCode}",' \
                 r'"authDate": "{authDate}"}}'.format(orgCode=QianHai.org_code,
                                                      chnlId=QianHai.chnl_id,
                                                      transNo=trans_no,
                                                      transDate=trans_date,
                                                      authCode=QianHai.auth_code,
                                                      authDate=trans_date)
        return header

    @staticmethod
    def format_json_enc_busi_data(**kwargs):
        origin_bus_data = r'{{' \
                          r'"batchNo": "{batchNo}",' \
                          r'"records":[{{' \
                          r'"idNo": "{personal_id}",' \
                          r'"idType": "0",' \
                          r'"name": "{user_name_cn}",' \
                          r'"mobileNo": "{mobile_num}",' \
                          r'"cardNo": "{card_id}",' \
                          r'"reasonNo": "04",' \
                          r'"email": "{email}",' \
                          r'"weiboNo": "{weibo_id}",' \
                          r'"weixinNo": "{wechat_id}",' \
                          r'"qqNo": "{qq_id}",' \
                          r'"taobaoNo": "{taobao_id}",' \
                          r'"jdNo": "{jd_id}",' \
                          r'"amazonNo": "{amazon_id}",' \
                          r'"yhdNo": "{yhd_id}",' \
                          r'"entityAuthCode": "{auth_code}",' \
                          r'"entityAuthDate": "{auth_date}",' \
                          r'"seqNo": "{seq_no}"}}]' \
                          r'}}'.format_map(SafeSub(kwargs))
        enc_busi_data = DataSecurityUtil.encrypt(origin_bus_data.encode(), QianHai.check_sum)
        return enc_busi_data

    @staticmethod
    def format_json_busi_data(enc_busi_data):
        busi_data = '"busiData": "' + enc_busi_data + '"'
        return busi_data

    @staticmethod
    def format_json_security_info(enc_busi_data):
        signature = DataSecurityUtil.sign_data(enc_busi_data)
        password = DataSecurityUtil.digest(QianHai.user_password.encode())
        security_info = r'"securityInfo":{{' \
                        r'"signatureValue": "{signatureValue}",' \
                        r'"userName": "{userName}",' \
                        r'"userPassword": "{userPassword}"' \
                        r'}}'.format(userName=QianHai.user_name,
                                     userPassword=password,
                                     signatureValue=signature)
        return security_info

    def __format_json_xhd(self, *args, **kwargs):
        pass

    @staticmethod
    def send_json_with_https(surl, json_str):
        j = json.loads(json_str)
        result = requests.post(surl, json=j, headers=QianHai.headers)
        return result
