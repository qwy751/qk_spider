import base64
from unittest import TestCase

# -*- coding: utf-8 -*-
from cryptography.hazmat.primitives.asymmetric import rsa

from app.datasource.qianhai.dataSecurityUtil import DataSecurityUtil


class TestDataSecurityUtil(TestCase):
    key = 'SK803@!QLF-D25WEDA5E52DA'
    origin_message = '{"batchNo":"33adfsf323233","records":[{"reasonCode":"01",' \
                     '"idNo":"362528198745421654","idType":"0","name":"唐唐","seqNo":"r231545334545"}]}'.encode()

    def test_digest(self):
        result = DataSecurityUtil.digest('weblogic1'.encode())
        assert result == 'af8f60dd67906ac8287ba38343ee5f6b821ce6d9'

    def test_sign_data(self):
        encry = DataSecurityUtil.encrypt(TestDataSecurityUtil.origin_message, TestDataSecurityUtil.key)
        result = DataSecurityUtil.sign_data(encry)
        assert result == 'VwWMJsJeXlJXAiKHj6M9ZLZ09oPjiOELF/CYRI1tctQH' \
                                  'jvugc4Td8PJjlmjFz4yZZXuN/cYUoRuQR7YRvpgaD' \
                                  'M/MWQZxpL1O0jaTmTsEZxWcwrnpA+lZeh9GZh6WaMFG6c' \
                                  'vwy2x6aEZML0z3vRQocuvbnlwU4u9eZvlugFBUP2o='


    def test_get_public_key(self):
        public_key = DataSecurityUtil.get_public_key()
        assert isinstance(public_key, rsa.RSAPublicKey)

    def test_verify_data(self):
        # DataSecurityUtil.verify_data()
        pass

    def test_get_private_key(self):
        DataSecurityUtil.get_private_key()

    def test_encrypt(self):
        encry = DataSecurityUtil.encrypt(TestDataSecurityUtil.origin_message, TestDataSecurityUtil.key)
        assert encry == 'OHQMWgf3em8ngz2z3KIG+7jdAUksdWvBDHRfmifPF66qWqnR' \
                        'ugeI/VgzgH1GC+2vFvFK/hHVayFDpoIB5ySok2N2tc10p+Ig' \
                        'UGbGcr7P64JJ6EpRB7e6lBNThe/UTQHtpejMVprg2F/07jqx' \
                        'yUdDAHH1w+aMOz69N/elrujlA1SiAWrDe9utHzmShKOEa+s+'

    def test_decrypt(self):
        abc = 'OHQMWgf3em8ngz2z3KIG+7jdAUksdWvBDHRfmifPF66qWqnRugeI/VgzgH1GC+2vF' \
              'vFK/hHVayFDpoIB5ySok2N2tc10p+IgUGbGcr7P64JJ6EpRB7e6lBNThe/UTQHtpe' \
              'jMVprg2F/07jqxyUdDAHH1w+aMOz69N/elrujlA1SiAWrDe9utHzmShKOEa+s+'.encode()
        message = DataSecurityUtil.decrypt(abc, TestDataSecurityUtil.key)
        assert message.decode() == TestDataSecurityUtil.origin_message


if __name__ == '__main__':
    # busi_data = '{"batchNo": "33adfsf323233", "records": [{"reasonCode": "01", "idNo": "362528198745421654", "idType": "0", "name": "唐唐", "seqNo": "r231545334545"}]}'
    busi_data = 'nimadeqianhaifuckqianhaiNMDCNMDQIANHAILAJIBITCHTHISisenoughlong'
    enc_busi_data = DataSecurityUtil.encrypt(busi_data.encode(), TestDataSecurityUtil.key)
    sig_value = DataSecurityUtil.sign_data(enc_busi_data).decode()
