# -*- coding: utf-8 -*-
import copy
import inspect
import json
import logging
import os
import os.path
import queue

from datetime import timedelta, datetime

import concurrent
import jpype


import xmltodict
from lxml import etree
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from suds.client import Client

from app.datasource.models import OriginData
from app.datasource.third import Third
from app.datasource.utils.tools import params_to_dict, SafeSub
from app.util.logger import logger
from config import DevelopmentConfig
from ..configuration import config
from ..utils.tools import convert_dict
from ...util.jvm import start_jvm

class FORMAT:
    JSON = 1


class PengYuan(Third):
    """
     获取鹏元数据工具类
    """
    params_mapping = {
        'user_name_cn': 'name',
        'personal_id': 'documentNo',
        'query_reason_id': 'queryReasonID',
        'card_id': 'cardNos',
        'begin_date': 'beginDate',
        'end_date': 'endDate',
        'card_id': 'accountNo',
        'mobile_num': 'mobile',
        'py_open_bank_id': 'cardNos',
        'license_no': 'licenseNo',
        'car_type': 'carType'
    }

    py_config = config.get('pengyuan')
    url = py_config.get('url')
    user_name = py_config.get('user_name')
    password = py_config.get('password')
    source = py_config.get('source')

    db_path = DevelopmentConfig.SQLALCHEMY_DATABASE_URI
    engine = create_engine(db_path, convert_unicode=True)
    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine))
    Base = declarative_base()
    Base.query = db_session.query_property()

    def __init__(self):
        self.Base.metadata.create_all(bind=self.engine)
        # self.client = Client(PengYuan.url)

    def create_query_condition(self, query_code, query_type=None, **kwargs):
        """
        生成查询条件,如果没有给定kwargs值, 该函数必须在query_内调用,根据外层函数参数自动生成查询条件
        :return:
        """
        if not len(kwargs):
            kwargs = params_to_dict(2)

        if not query_type:
            result = self.__params_dict_condition_xml(query_code, **kwargs)
        elif query_type == FORMAT.JSON:
            result = self.__params_dict_condition_json(query_code, **kwargs)

        return result

    def __params_dict_condition_xml(self, query_code, **kwargs):
        """
        将字典转换为xml的查询条件
        :param query_code:
        :param kwargs:
        :return:
        """
        query_template = '<?xml version="1.0" encoding="GBK"?>' \
                         '<conditions>' \
                         '<condition queryType="{}">' \
                         '</condition>' \
                         '</conditions>'.format(query_code).encode()
        query_t = self.__to_xml(query_template)
        condition_reg = "//conditions/condition"
        condition = query_t.xpath(condition_reg)[0]
        for n, v in kwargs.items():
            item = etree.SubElement(condition, 'item')
            name = etree.SubElement(item, 'name')
            name.text = n
            value = etree.SubElement(item, 'value')
            value.text = v
        result = etree.tostring(query_t, encoding='unicode')
        return result

    def __params_dict_condition_json(self, query_code, **kwargs):
        """
        将字典转换为json的查询条件
        :param query_code:
        :param kwargs:
        :return:
        """
        kwargs['query_code'] = query_code
        template = r'{{' \
                   r'"conditions": {{' \
                   r'"condition": {{' \
                   r'"interfaceId": "{query_code}",' \
                   r'"item": [{{' \
                   r'"name": "beginDate",' \
                   r'"value": "{beginDate}"}},' \
                   r'{{"name": "endDate",' \
                   r'"value": "{endDate}"}},' \
                   r'{{"name": "queryType",' \
                   r'"value": "{queryType}"}},' \
                   r'{{"name": "monitorStr",' \
                   r'"value": "{monitorStr}"}},' \
                   r'{{"name": "page",' \
                   r'"value": "{page}"}},' \
                   r'{{"name": "pageCount",' \
                   r'"value": "{pageCount}"}},' \
                   r'{{"name": "applyID",' \
                   r'"value": "{applyID}"}}' \
                   r']' \
                   r'}}' \
                   r'}}' \
                   r'}}'.format_map(SafeSub(kwargs))
        j = json.loads(template)
        return j

    def query(self, *args, **kwargs):
        """
        查询接口
        :param result:
        :param args:
        :param kwargs: 查询的参数
        :return:
        """
        kwargs = self.pre_query_params(*args, **kwargs)
        # TODO:子报告如何处理
        result = queue.Queue()
        threads = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=18) as executor:
            func_params = {func[1]: {param: kwargs.get(param) for param
                                     in inspect.signature(func[1]).parameters.keys()
                                     if kwargs.get(param) is not None}
                           for func in inspect.getmembers(self, predicate=inspect.ismethod)
                           if func[0].startswith('query_')}

            future_func = {executor.submit(func, **func_params[func]) for func in func_params.keys()}
            try:
                for future in concurrent.futures.as_completed(future_func, 15):
                    try:
                        data = future.result()
                        result.put(data)
                    except Exception as exc:
                        logger.error(exc)
            except TimeoutError as te:
                logger.error(te)

        result_final = []
        while True:
            try:
                data = result.get_nowait()
                if data:
                    result_final.append(data)
            except queue.Empty:
                break
        return result_final, self.source

    def __query(self, condition, *args, **kwargs):
        """
        根据条件申请查询
        :param condition: 查询条件
        :return: 查询结果,返回查询到的值
        """

        # self.client.set_options(port='WebServiceSingleQuery')
        # TODO: 测试时不调用
        # bz_result = self.client.service.queryReport(self.user_name, self.password, condition, 'xml') .encode('utf-8').strip()

        bz_result = b'<result>\r\n\t<status>1</status>\r\n\t<returnValue>UEsDBBQACAAIADZxXEkAAAAAAAAAAAAAAAALAAAAcmVwb3J0cy54bWx9U09rE0EcPVfwOwxzaqF1d7ZJG8tkC8YqRayQ1A+w3UybJclMurMb\nG79Nkx4UC2pFYv+o+KeYEGi2SCKI1YMHESnqRQ9CcXZ2k9pkcQ+7M29n3vu995vBs2vFAigTm1uMJiG6oEJAqMmyFl1JwquXrkEwq58/h02L\np0mJ2Q4HYMlwFlgSaiqaQqo2jRKq/8QhcKnlLBhFkoRvNp8/rt1ptndqtbtPfzTee/vtav3k4Od2s3701mt/3L7XegYBd5du2CuG0D34/WCr\ncbx3cujVq13Pew3Bqkvsyk1O7PnLSbiav8UlEOIp5lJHVAuBTUxilcmi5av2KgIoMaMmZmIJeKZ0sdj/+ITDtS+5ViE7R7OnTBNInehzxWOh\ndJoYnFGfA6lIWgjIFyslwn1wSo2No5imiiAdmxhOmnC3IIpVx9XB5ZmcGKWMkhNkv15tHtePGu3uxqikGQPaevXJr0ar/qXd2f387oOf4qjk\nHgMQ5AyeqXCHFOdsm9lJuGwUOIHA4ldsdpvQHiAiGMFhajRr+Vrcx0awJfbK0Qimomu6/8KKHAaoGZSmP9zd+np4v/PJ67z6g5UeGqwpGwWX\n6K3vL6qPNrESzCS70qcfEsoy0y0SKk7Rf+W6G3snO/svv0VLaiJ/FEMXE9Mq0uJIm9Si5bEybB6XWMEySSpHzLw2T5fZ2cYEbZwcaFeKcSds\n8EBrNXFn/B5cJ5wbK2J7EPppANJkL6O+Y3yaQ6Sbf37L5baU0yexEo4kWsoxh+lYCb7ScCgssAGb0rq464ymLZ7POIYTaT44vVHmI851pHkh\nPSQj4f5lPDvj+l9QSwcINagM0moCAACJBAAAUEsBAhQAFAAIAAgANnFcSTWoDNJqAgAAiQQAAAsAAAAAAAAAAAAAAAAAAAAAAHJlcG9ydHMu\neG1sUEsFBgAAAAABAAEAOQAAAKMCAAAAAA==</returnValue>\r\n</result>'

        # try:
        #     # r = OriginData(request_time=datetime.now(), source='pengyuan',
        #     #                source_request=condition, source_result=bz_result)
        #     # self.db_session.add(r)
        #     # self.db_session.commit()
        #     # print('arrived at here')
        # except Exception as ex:
        #     print(ex)

        # print(bz_result)
        result = self.__format_result(bz_result)
        return result

    @staticmethod
    def __to_xml(bz_result):
        """
        将查询的字符串转换为xml结点
        :param bz_result:
        :return:
        """
        try:
            xml_data = etree.fromstring(bz_result)
            return xml_data
        except ValueError as e:
            logging.error("结果转换xml失败{}!", e)

    @staticmethod
    def __get_result_code(xml_result):
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
            log = u"查询异常!异常代码:{}, 错误信息:{}".format(err_code, err_message)
            logging.error(log)
            return
        rv = self.__get_result_value(xml_result)
        return rv

    def __get_result_value(self, xml_result):
        """
        获取结果中处理过的值
        :param bz_result:
        :return:
        """
        data = xml_result.find('returnValue').text
        rv = self.__format_result_value(data)
        # rv = xmltodict.parse(rv, dict_constructor=dict, xml_attribs=False)
        return rv

    def __format_result_value(self, data):
        """
        对查询到结果结果进行解码
        :return:
        """
        try:
            start_jvm()
            z_result = self.__base64_decode(data)
            rv = self.__unzip(z_result)
            return rv
        except Exception as ex:
            logger.error(ex)

    @staticmethod
    def __base64_decode(data):
        """
        鹏元元的base64解码
        :param data: resultValue原始字段内容
        :return: 解码后的内容
        """
        try:
            Base64 = jpype.JPackage('cardpay').pengyuan.Base64
            b64 = Base64()
            z_result = b64.decode(data)
            return z_result
        except Exception as ex:
            logger.error(ex)

    @staticmethod
    def __unzip(z_result):
        """
        鹏元的解压缩
        :param z_result: 未解压缩的内容
        :return: 解压缩后的内容
        """
        try:
            Cs = jpype.JPackage('cardpay').pengyuan.CompressStringUtil
            rv = Cs.decompress(z_result)
            return rv
        except Exception as ex:
            logger.error(ex)

    def query_personal_id_risk(self, name, documentNo, subreportIDs='10604', queryReasonID='101', refID=None):
        """
        个人身份认证信息/风险信息查询
        :param name: 姓名
        :param documentNo: 身份证号
        :param subreportIDs: 子查询
        :param queryReasonID: 查询原因
        :param refID: 引用ID
        :return: 查询结果
        """
        report = self.__query(self.create_query_condition(25160))
        from .transform import process_person_id_risk
        process_person_id_risk(documentNo, report, self.db_session)
        return report

    def query_card_pay_record(self, name, cardNos, beginDate=None, endDate=None,
                              subreportIDs='14501,14512', queryReasonID='101', documentNo=None, refID=None):
        """
        卡多笔交易记录验请求xml规范
        :param name:
        :param cardNos:
        :param beginDate:
        :param endDate:
        :param subreportIDs:
        :param queryReasonID:
        :param documentNo:
        :param refID:
        :return:
        """
        kwargs = {}
        if beginDate is None and endDate is None:
            kwargs = params_to_dict(1)
            current_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            d_time = timedelta(days=300)
            one_year_ago = (datetime.now() - d_time).strftime('%Y-%m-%d')
            kwargs['beginDate'] = one_year_ago
            kwargs['endDate'] = current_date

        return self.__query(self.create_query_condition(25197, **kwargs))

    def query_career_capacity(self, name, documentNo, subreportIDs='13400', queryReasonID='101', refID=None):
        """
        职业资格查询接口文档
        :param name:
        :param documentNo:
        :param subreportIDs:
        :param queryReasonID:
        :param refID:
        :return:
        """
        return self.__query(self.create_query_condition(25121))

    def query_personal_enterprise_telephone(self, tel, subreportIDs='21603',
                                            queryReasonID='101', ownerName=None, refID=None):
        """
        个人和企业信息查询
        :param mobile:
        :param subreportIDs:
        :param queryReasonID:
        :param ownerName:
        :param refID:
        :return:
        """
        return self.__query(self.create_query_condition(25129))

    def query_personal_revenue_assess(self, name, documentNo, corpName, positionName=None, subreportIDs='14003',
                                      queryReasonID='101', topDegree=None, graduateYear=None,
                                      college=None, fullTime=None, refID=None):
        """
        个人收入测评
        :param name:
        :param documentNo:
        :param corpName:
        :param positionName:
        :param subreportIDs:
        :param queryReasonID:
        :param topDegree:
        :param graduateYear:
        :param college:
        :param fullTime:
        :param refID:
        :return:
        """
        # TODO: 没有开通
        return self.__query(self.create_query_condition(25180))

    def query_airplane_info(self, name, documentNo=None, passport=None, month='12', subreportIDs='14100',
                            queryReasonID='101', refID=None):
        """
        航空出行信息
        :param name:
        :param documentNo:
        :param passport:
        :param month:
        :param subreportIDs:
        :param queryReasonID:
        :param refID:
        :return:
        """
        return self.__query(self.create_query_condition(25175))

    def query_personal_enterprise_risk(self, name, subreportIDs='14200', queryReasonID='101', refID=None):
        """
        个人与企业风险汇总信息
        :param name:
        :param subreportIDs:
        :param queryReasonID:
        :param refID:
        :return:
        """
        return self.__query(self.create_query_condition(25136))

    def query_personal_bank_info(self, name, documentNo, mobile, accountNo,
                                 openBankNo=None, subreportIDs='14506', queryReasonID='101', refID=None):
        """
        查询个人银行账户核查信息
        :param name:
        :param documentNo:
        :param accountNo:
        :param openBankNo:
        :param mobile:
        :param subreportIDs:
        :param queryReasonID:
        :param refID:
        :return:
        """
        return self.__query(self.create_query_condition(25173))

    def query_open_bank_info(self, accountNo, subreportIDs='14514', queryReasonID='101', refID=None):
        """
        开户行信息查询
        :param accountNo:
        :param subreportIDs:
        :param queryReasonID:
        :param refID:
        :return:
        """
        return self.__query(self.create_query_condition(25193))

    def query_personal_last_two_years_info(self, name, documentNo, subreportIDs='19901', queryReasonID='101',
                                           refID=None):
        """
        个人近两年查询记录
        :param name:
        :param documentNo:
        :param subreportIDs:
        :param queryReasonID:
        :param refID:
        :return:
        """
        return self.__query(self.create_query_condition(25136))

    def query_enterprise_last_one_year(self, corpName, subreportIDs='20901', queryReasonID='101', refID=None):
        """
        企业近一年查询记录,
        :param corpName:
        :param subreportIDs:
        :param queryReasonID:
        :param refID:
        :return:
        """
        return self.__query(self.create_query_condition(25123))

    def query_enterprise_operation(self, corpName=None, registerNo=None, subreportIDs='22300', queryReasonID='101',
                                   refID=None):
        """
        企业经营指数
        :param corpName: 被查询企业名称
        :param registerNo: 被查询工商注册号
        :param subreportIDs:
        :param queryReasonID:
        :param refID:
        :return:
        """
        return self.__query(self.create_query_condition(25123))

    def query_trade_company_reprot(self, corpName, queryMonth='12', subreportIDs='22601', queryReasonID='101',
                                   refID=None):
        """
        商户经营分析
        :param corpName:
        :param queryMonth:
        :param subreportIDs:
        :param queryReasonID:
        :param refID:
        :return:
        """
        return self.__query(self.create_query_condition(25179))

    def query_risk_info(self, beginDate, endDate, applyID,
                        monitorStr, page=1, queryType=4, pageCount=100, queryReasonID='py020'):
        """
        风险信息监控接口
        :param interfaceId: 查询接口id（必填），py020为个人和企业监控结果查询接口。
        :param queryType:  查询类型（必填）：
                                    1:查询符合条件内所有个人的监控信息结果
                                    2:查询符合条件内所有企业的监控信息结果
                                    3:查询符合条件内所有个人和企业的监控信息结果
                                    4:查询符合条件内指定个人或企业的监控信息结果
                            说明：符合条件是指处于监控中的名单，或过期及取消后还在缓存查询天数内的监控过的名单，
                            如果20150101过期，缓存查询天数为10天，
                            那么20150111还可以查询20140101到20150101这一个周期的历史监控信息，
                            如果超过20150111就不在让查询历史，同样取消也是如此，如果20140101开始监控，20140501取消监控，
                            那么20150111还可以查到20140101到20140501这段监控时间内的历史监控信息，
                            如果超过20150111就不在让查询历史，并且只支持单个周期查询，不能跨周期查。
        :param beginDate: 查询监控开始日期（选填） ,时间格式：yyyyMMdd , 监控开始时间为T+1，如20150423将个人或企业加入监控名单，
        则20150424开始执行监控，20150425可以查询20150423的新增及变更的数据。
        :param endDate: 查询监控结束日期时间（选填）, 格式：yyyyMMdd
        :param monitorStr: 监控名单（查询类型为4时必填） 如：
                            1,张三,4678979846133 (参数1)数据类型：1：个人 2：企业 ,
                            (参数2)名称：姓名和企业名称（数据类型是个人时为姓名，数据类型是企业时为企业名称） ,
                            (参数3)证件号码：身份证号码（数据类型是个人时才有值，数据类型是企业时该处为空）
                          说明：参数之间用英文逗号分隔，多组参数之间用英文分号分隔, 如：
                              1,张三,4678979846133;
                              1,李四,4678979846133
                          注意：
                          1. 当查询类型为4时，此字段不能为空，
                          2.当前查询类型为其它值时，此字段为空，
                          则会查询所有的信息(如开始时间，结束时间不为空，则查询监控加入时间为该日期内的名单)
        :param page: 页码（必填）
        :param pageCount: 每页记录数（必填）, 说明：取值应当大于0小于等于100
        :param applyID: 申请ID（必填），同一个申请ID最多可以调用该接口二十次。
        :return:
        """
        # TODO:没有这个接口了
        return self.__query(self.create_query_condition(queryReasonID, query_type=FORMAT.JSON))

    def query_enterprise_info(self, corpName=None, orgCode=None, registerNo=None,
                              subreportIDs='95004',
                              queryReasonID='101', refID=None):
        """
        企业信息查询
        :return:
        """
        return self.__query(self.create_query_condition(25123))

    def query_car_info(self, name, documentNo, licenseNo, carType='02',
                       subreportIDs='13812', queryReasonID='101', refID=None):
        """
        全国车辆信息核查
        :param name:
        :param documentNo:
        :param licenseNo:
        :param carType:
        :param queryReasonID:
        :param subreportIDs:
        :param refID:
        :return:
        """
        return self.__query(self.create_query_condition(25200))

    def query_mini_loan_rish_grade(self, name, documentNo, province, city, corpName, positionName,
                                   applyMoney='10000', applyPeriod='12',
                                   returnAmountBank=None, returnAmountLoan=None,
                                   contact=None, emersencyContact=None, subreportIDs='91203',
                                   queryReasonID='101', refID=None):
        """
        小额贷款风险评分
        :param name:
        :param documentNo:
        :param applyMoney:
        :param applyPeriod:
        :param returnAmountBank:
        :param returnAmountLoan:
        :param contact:
        :param emersencyContact:
        :return:
        """
        return self.__query(self.create_query_condition(25184))

    @staticmethod
    def format_result(xml_data):
        """
        处理查询结果,提取需要的信息
        :param xml_data: xml格式的查询结果
        :return:
        """
        # TODO: 先简单处理,之后在完善,未完成
        xml_result = etree.fromstring(xml_data)
        cisReport = xml_result.find('cisReports/cisReport')
        hasSystemError = bool(cisReport.get('hasSystemError'))
        isFrozen = bool(cisReport.get('isFrozen'))
        if hasSystemError and isFrozen:
            return

        result = {}
        for item in cisReport.items():
            if item.tag == 'queryConditions':
                continue
            item_dict = {}
            if item.get('treatResult') == '1':
                item_dict1 = {}
                for item1 in item.items():
                    if item1.tag == 'item':
                        pass

    def create_file(self, condition, result, query_type, *args):
        """
        该函数废弃
        :param condition:
        :param result:
        :param query_type:
        :param args:
        :return:
        """
        basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        file_dir = basedir + '/result/' + str(query_type) + '/'
        if not os.path.exists(file_dir):
            os.mkdirs(file_dir)
        file_path = file_dir + str(condition.get('documentNo'))
        for ar in args:
            file_in = file_path + ar
            file_out = file_path + ar
        file_in += '_in.xml'
        file_out += '_out.xml'

        if result is not None:
            with open(file_in, 'wb') as fi:
                fi.write(condition.encode('utf-8'))

            with open(file_out, 'wb') as fo:
                fo.write(result.encode('utf-8'))


if __name__ == '__main__':
    # py = PengYuan()
    # py.test_query_personal_id_risk(name=u'阎伟晨', documentNo='610102199407201510')
    pass
