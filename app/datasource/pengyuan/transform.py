# -*- coding: utf-8 -*-
from lxml import etree
import sys
import xmltodict
from app.info import *
from app.util.logger import logger
from sqlalchemy.exc import StatementError

sys.path.append("..")


def __remove_xml_head(xml_string):
    """
    去除xml文档头部
    :param xml_string: 完整xml文档内容
    :return: 去除xml头部的字符串
    """
    index = xml_string.find('>')
    if xml_string[index - 1] is '?':
        return xml_string[index + 1:].strip()
    else:
        return xml_string.strip()


def __get_report_dict(report, path):
    """
    将结果报告中选取节点转换为字典
    :param report: 结果报告
    :param path:  选取内容路径
    :return: 结果字典
    """
    document = etree.XML(__remove_xml_head(report))
    result_report = document.find(path)
    if result_report is None:
        return None
    selected = etree.tostring(result_report, encoding='UTF-8')
    return xmltodict.parse(selected, xml_attribs=False)


def create_person(name, identity, db_session):
    """
    创建个人
    :param name: 姓名
    :param identity: 身份证
    :param db_session: 数据库会话
    :return: 无返回，在Person表新建记录
    """
    person = Person(name=name, identity=identity)
    # 存个人信息
    try:
        db_session.add(person)
        db_session.commit()
    except StatementError as e:
        logger.error(e)


def process_person_id_risk(identity, report, db_session):
    """
    处理个人身份认证信息及风险信息
    :param identity：身份证
    :param report: 鹏元查询接口返回数据
    :param db_session: 数据库会话
    :return: 无返回值，将结果存入Person
    """
    selected_dict = __get_report_dict(report, 'cisReport/policeCheck2Info/item')
    if selected_dict is None:
        return
    # 写入个人基本信息表
    person = db_session.query(Person).filter_by(identity=identity).first()
    person.name = selected_dict['item']['name']
    person.photo = selected_dict['item']['photo']
    person.identity_status = selected_dict['item']['result']
    try:
        db_session.add(person)
        db_session.commit()
    except StatementError as e:
        logger.error(e)

    # 个人风险分析
    risk_dict = __get_report_dict(report, 'cisReport/personRiskStatInfo/stat')
    if risk_dict is None:
        return
    person_risk = db_session.query(PersonRisk).filter_by(person_id=person.id).first()
    if person_risk is None:
        person_risk = PersonRisk(person=person)
    person_risk.judicial_case = risk_dict['stat']['alCount']
    person_risk.judicial_performed = risk_dict['stat']['zxCount']
    person_risk.judicial_blacklist = risk_dict['stat']['sxCount']
    person_risk.tax_performed = risk_dict['stat']['swCount']
    person_risk.tax_debt = risk_dict['stat']['cqggCount']
    person_risk.loan_expired = risk_dict['stat']['wdyqCount']
    try:
        db_session.add(person_risk)
        db_session.commit()
    except StatementError as e:
        logger.error(e)


def process_air_traffic(identity, report, db_session):
    """
    航空出行
    :param identity 被查询证件号
    :param report: 查询结果
    :param db_session: 数据库会话
    :return: 无返回值
    """
    select_dict = __get_report_dict(report, 'cisReport/AirTktInfo/item')
    if select_dict is None:
        return
    person = db_session.query(Person).filter_by(identity=identity).first()
    air_info = AirTraffic.query.filter_by(person_id=person.id).first()
    if air_info is None:
        air_info = AirTraffic(person=person)
    air_info.most_month = select_dict['item']['mostMonth']
    air_info.most_month_percent = select_dict['item']['mostMonthPercent']
    air_info.avg_discount_area = select_dict['item']['avgDiscountArea']
    air_info.business_cabin_percent = select_dict['item']['businessCabinPercent']
    air_info.official_cabin_percent = select_dict['item']['officialCabinPercent']
    air_info.economy_cabin_percent = select_dict['item']['economyCabinPercent']
    air_info.from_city = select_dict['item']['fromCity']
    air_info.from_city_percent = select_dict['item']['fromCityPercent']
    air_info.dest_city = select_dict['item']['destCity']
    air_info.dest_city_percent = select_dict['item']['destCityPercent']
    air_info.most_airline = select_dict['item']['mostAirline']
    air_info.most_airline_percent = select_dict['item']['mostAirlinePercent']
    air_info.domestic_percent = select_dict['item']['domesticPercent']
    air_info.inter_percent = select_dict['item']['interPercent']
    air_info.free_percent = select_dict['item']['freeCountArea']
    air_info.avg_price = select_dict['item']['avgPrice']
    air_info.avg_delay_area = select_dict['item']['avgDelayArea']
    air_info.avg_ticket_day_area = select_dict['item']['avgTicketDayArea']
    air_info.last_flight_date_area = select_dict['item']['lastFlightDateArea']
    air_info.fly_count_level = select_dict['item']['flyCountLevel']
    air_info.fly_count_name = select_dict['item']['flyCountName']
    air_info.fly_count_area = select_dict['item']['flyCountArea']
    air_info.grade_desc = select_dict['item']['gradeDesc']
    air_info.cabin_desc = select_dict['item']['cabinDesc']
    air_info.fly_score = select_dict['item']['flyScore']
    air_info.cabin_score = select_dict['item']['cabinScore']
    try:
        db_session.add(air_info)
        db_session.commit()
    except StatementError as e:
        logger.error(e)


def process_person_query_last_two_years(identity, report, db_session):
    """
    个人近两年查询记录
    :param identity 被查询证件号
    :param report: 查询结果
    :param db_session: 数据库会话
    :return: 无返回值
    """
    select_dict = __get_report_dict(report, 'cisReport/historyQueryInfo')
    if select_dict is None:
        return
    person = db_session.query(Person).filter_by(identity=identity).first()
    for node in select_dict['historyQueryInfo']['item']:
        info = PersonQueried(person=person)
        info.unit = node['unit']
        info.unit_member = node['unitMember']
        info.query_date = node['queryDate']
        try:
            db_session.add(info)
            db_session.commit()
        except StatementError as e:
            logger.error(e)


if __name__ == '__main__':
    # app = create_app('testing')
    # app_context = app.app_context()
    # app_context.push()
    # db.create_all()
    # process_person_id_risk(test)
    pass
