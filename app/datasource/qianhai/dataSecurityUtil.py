# -*- coding: utf-8 -*-
import base64
import os

import binascii
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding as primitives_padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding as asymmetric_padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import jks
import textwrap


class DataSecurityUtil:

    base = os.path.abspath(os.path.dirname(__file__))

    @staticmethod
    def get_pem(der_bytes, type):
        result = "-----BEGIN {type}-----\r\n" \
                 "{data}\r\n" \
                 "-----END {type}-----".format(type=type,
                                               data="\r\n".join(textwrap.wrap(
                                                   base64.b64encode(der_bytes).decode('ascii'), 64)))
        return result

    @staticmethod
    def get_public_key(file_path=None):
        """
        获取er后缀的公钥
        :param file_path: 文件路径
        :return:
        """
        if not file_path:
            file_path = DataSecurityUtil.base + '/credoo_stg.cer'

        with open(file_path, 'rb') as f:
            cert = x509.load_der_x509_certificate(f.read(), default_backend())
            public_key = cert.public_key()
        return public_key

    @staticmethod
    def get_private_key(file_path=None):
        """
        获取jks后缀的私钥
        :return:
        """
        if not file_path:
            file_path = DataSecurityUtil.base + '/credoo_stg.jks'
        ks = jks.KeyStore.load(file_path, 'qhzx_stg')
        pk = ks.private_keys.get('signkey')

        if pk.algorithm_oid == jks.util.RSA_ENCRYPTION_OID:
            p_key = DataSecurityUtil.get_pem(pk.pkey, "RSA PRIVATE KEY")

        private_key = serialization.load_pem_private_key(p_key.encode(),
                                                         password=None,
                                                         backend=default_backend())

        certificate = DataSecurityUtil.get_pem(pk.cert_chain[0][1], "CERTIFICATE")
        cert = x509.load_pem_x509_certificate(certificate.encode(), default_backend())
        return private_key, cert

    @staticmethod
    def sign_data(data):
        private_key, _ = DataSecurityUtil.get_private_key()
        sign = private_key.sign(data, asymmetric_padding.PKCS1v15(), hashes.SHA1())
        result = base64.b64encode(sign)
        return result

    @staticmethod
    def verify_data(data, sign_value):
        # TODO: 未测试
        public_key = DataSecurityUtil.get_public_key()
        signature = base64.decode(sign_value)
        result = public_key.verify(signature,
                                   data,
                                   asymmetric_padding.PKCS1v15(),
                                   hashes.SHA1())
        return result

    @staticmethod
    def digest(ori_byte):
        # binascii
        digest = hashes.Hash(hashes.SHA1(), default_backend())
        digest.update(ori_byte)
        d = binascii.hexlify(digest.finalize()).decode()
        return d

    @staticmethod
    def encrypt(origin, key):
        """
        加密，算法3DES，模式：ECB
        :param origin: 待加密的bytes
        :param key: 密钥
        :return: 加密后的BASE64编码
        """
        cipher = Cipher(algorithms.TripleDES(key), modes.ECB(), default_backend())
        encryptor = cipher.encryptor()
        padder = primitives_padding.PKCS7(64).padder()
        padder_data = padder.update(origin) + padder.finalize()
        print(len(padder_data))
        ct = encryptor.update(padder_data) + encryptor.finalize()
        result = base64.b64encode(ct)
        return result

    @staticmethod
    def decrypt(data, key):
        """
        解密：算法：3DES
        :param data: 待解密bytes
        :param key: 密钥
        :return: 解密厚的bytes
        """

        data = base64.b64decode(data)
        cipher = Cipher(algorithms.TripleDES(key), modes.ECB(), default_backend())
        decryptor = cipher.decryptor()
        origin = decryptor.update(data) + decryptor.finalize()
        unpadder = primitives_padding.PKCS7(64).unpadder()
        origin_result = unpadder.update(origin) + unpadder.finalize()
        return origin_result
