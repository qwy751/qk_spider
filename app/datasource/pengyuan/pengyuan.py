# -*- coding: utf-8 -*-
import os
from suds.client import Client
import logging
import io
from lxml import etree

import jpype
import os.path

import pydevd

pydevd.settrace('licho.iok.la', port=44957, stdoutToServer=True, stderrToServer=True)

basedir = os.path.abspath(os.path.dirname(__file__))

logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)


class PengYuan:
    '''
    获取鹏元数据工具类
    '''

    URL = "http://www.pycredit.com:9001/services/WebServiceSingleQuery?wsdl"
    USER_NAME = 'qkwsquery'
    PASSWORD = 'qW+06PsdwM+y1fjeH7w3vw=='

    def __init__(self):
        self.jvm_path = jpype.getDefaultJVMPath()
        basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        jar_path = basedir + '/pengyuan.jar'
        self.jvmArg = "-Djava.class.path=" + jar_path
        self.client = Client(PengYuan.URL)

    def start_jvm(self):
        try:
            if jpype.isJVMStarted():
                jpype.shutdownJVM()
            jpype.startJVM(self.jvm_path, '-ea', self.jvmArg)
        except InterruptedError as e:
            logging.debug("JVM启动失败{}", e)

    def stop_jvm(self):
        jpype.shutdownJVM()

    def create_query_condition(self, query_code, **kwargs):
        """
        生成查询条件
        :return:
        """
        with io.open(basedir + '/id_test.xml', 'r', encoding='GBK') as c:
            condition = c.read()
        return condition

    def query(self, condition):
        """
        根据条件申请查询
        :param condition: 查询条件
        :return: 查询结果,返回查询到的值
        """
        self.client.set_options(port='WebServiceSingleQuery')
        bz_result = self.client.service.queryReport(PengYuan.USER_NAME, PengYuan.PASSWORD, condition, 'xml') \
            .encode('utf-8').strip()
        result = self.__format_result(bz_result)
        return result

    def __to_xml(self, bz_result):
        """
        将查询的字符串转换为xml结点
        :param bz_result:
        :return:
        """
        try:
            xml_data = etree.fromstring(bz_result)
        except ValueError as e:
            logging.error("结果转换xml失败{}!", e)
        return xml_data

    def __get_result_code(self, xml_result):
        """
        获取结果中的结果代码
        :param xml_result:
        :return:
        """
        code = xml_result.find('status').text
        return int(code)

    def __format_result(self, bz_result):
        """
        格式化查询结果的原始数据
        :param bz_result:
        :return:
        """
        xml_result = self.__to_xml(bz_result)
        if self.__get_result_code(xml_result) != 1:
            err_code = xml_result.find('errorCode').text
            err_message = xml_result.find('errorMessage').text
            logging.error("查询异常!异常代码:{}, 错误信息:{}", err_code, err_message)
            return
        rv = self.__get_result_value(xml_result)
        return rv

    def __get_result_value(self, xml_result):
        """
        获取结果中处理过的值
        :param bz_result:
        :return:
        """
        data = bytes(xml_result.find('returnValue').text)
        rv = self.__format_result_value(data)
        return rv

    def __format_result_value(self, data):
        """
        对查询到结果结果进行解码
        :return:
        """
        self.start_jvm()
        z_result = self.__base64_decode(data)
        rv = self.__unzip(z_result)
        self.stop_jvm()
        return rv

    def __base64_decode(self, data):
        """
        鹏元元的base64解码
        :param data: resultValue原始字段内容
        :return: 解码后的内容
        """
        ta = jpype.JPackage('cardpay').Base64
        b64 = ta()
        z_result = b64.decode(data)
        return z_result

    def __unzip(self, z_result):
        """
        鹏元的解压缩
        :param z_result: 未解压缩的内容
        :return: 解压缩后的内容
        """
        cs = jpype.JPackage('cardpay').CompressStringUtil
        rv = cs.decompress(z_result)
        return rv

    def query_personal_id_risk(self, name, id, subreport_id, reason_id, ref_id=None):

        query_type = 25160
        sub_report = {10604: True, 10603: False, 14200: True}
        query_reason = {101: "货款审批",
                        102: "货款贷后管理",
                        103: "贷款催收",
                        104: "审核担保人信用",
                        105: "担保/融资审批",
                        202: "信用卡货后管理",
                        201: "信用卡审批",
                        203: "信用卡催收",
                        301: "加强税源基础管理",
                        302: "追缴欠税",
                        303: "商户信用",
                        304: "申报创新人才奖",
                        305: "失业人员小额贷款担保审批",
                        306: "深圳市外来务工人员积分入户申请",
                        401: "车货保证保险审批",
                        402: "审核国货保证保险担保人信用",
                        501: "求职",
                        502: "招聘",
                        503: "异议处理",
                        901: "了解个人信用",
                        999: "其他"
                        }

        query_template = '''
        <?xml version="1.0" encoding="GBK"?>
        <conditions>
            <condition queryType="25160">
                <item>
                    <name>name</name>
                    <value>阎伟晨</value>
                </item>
                <item>
                    <name>documentNo</name>
                    <value>610102199407201510</value>
                </item>
                <item>
                    <name>subreportIDs</name>
                    <value>10604</value>
                </item>
                <item>
                    <name>queryReasonID</name>
                    <value>101</value>
                </item>
                <item>
                    <name>refID</name>
                    <value>测试</value>
                </item>
            </condition>
        </conditions>
        '''



if __name__ == '__main__':
    py = PengYuan()
    condition = py.create_query_condition()
    result = py.query(condition)
    print(result)
