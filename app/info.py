# -*- coding: utf-8 -*-
"""
个人征信数据结构
"""

from app import db


class Person(db.Model):
    """
    被征信人基本信息
    """
    __tablename__ = 'person'
    id = db.Column(db.Integer, primary_key=True)
    # 姓名
    name = db.Column(db.String(64))
    # 身份证
    identity = db.Column(db.String(18), unique=True)
    # 照片
    photo = db.Column(db.Text)
    # 身份证验证情况
    identity_status = db.Column(db.String(50))
    # 出生日期
    birth = db.Column(db.Date)
    # 教育程度
    education = db.Column(db.Integer)
    # 性别
    sex = db.Column(db.String)
    # 住址
    address = db.Column(db.String(200))
    # 年龄
    age = db.Column(db.SmallInteger)
    # 婚姻状况
    marriage = db.Column(db.String(10))
    # 宗教
    religion = db.Column(db.String(20))
    # 家庭成员
    family = db.relationship('Family', backref='person')
    # 联系电话
    phone = db.relationship('Telephone', backref='person')
    # 工作单位
    unit = db.relationship('Unit', backref='person')
    # 房产
    estate = db.relationship('Estate', backref='person')
    # 租房情况
    lodging = db.relationship('Lodging', backref='person')
    # 个人风险
    person_risk = db.relationship('PersonRisk', backref='person')
    # 银行卡
    bank_card = db.relationship('BankCard', backref='person')
    # 投资情况
    investment = db.relationship('Investment', backref='person')
    # 贷款情况
    loan = db.relationship('Loan', backref='person')
    # 担保情况
    loan_guarantee = db.relationship('LoanGuarantee', backref='person')
    # 车辆信息
    vehicle = db.relationship('Vehicle', backref='person')
    # 经营企业
    company = db.relationship('Company', backref='person')
    # 个人近两年被查询记录
    person_queried = db.relationship('PersonQueried', backref='person')


class Family(db.Model):
    """
    家庭关系
    """
    __tablename__ = 'family'
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    # 关系
    relation = db.Column(db.String(10))
    # 姓名
    name = db.Column(db.String(64))
    # 身份证
    identity = db.Column(db.String(18), unique=True)
    # 出生日期
    birth = db.Column(db.Date, nullable=True)
    # 教育程度
    education = db.Column(db.Integer, nullable=True)
    # 性别
    sex = db.Column(db.String)
    # 住址
    address = db.Column(db.String(200))
    # 年龄
    age = db.Column(db.SmallInteger)
    # 宗教
    religion = db.Column(db.String(20))


class PersonQueried(db.Model):
    """
    个人被查询情况
    """
    __tablename__ = 'person_Queried'
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    # 查询单位
    unit = db.Column(db.Text)
    # 查询机构
    unit_member = db.Column(db.Text)
    # 查询时间
    query_date = db.Column(db.Text)


class Telephone(db.Model):
    """
    联系电话，部分对应鹏元个人和企业信息查询
    """
    __tablename__ = 'telephone'
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    # 电话号码
    number = db.Column(db.String(20))
    # 登记名字
    owner_name = db.Column(db.String(20))
    # 登记证件号
    owner_identity = db.Column(db.String(20))
    # 归属地
    address = db.Column(db.String(200))
    # 开通时间
    open_time = db.Column(db.DateTime)
    # 每月平均消费
    month_cost = db.Column(db.DECIMAL)


class Unit(db.Model):
    """
    单位
    """
    __tablename__ = 'unit'
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    # 单位名称
    name = db.Column(db.String(200))
    # 单位地址
    address = db.Column(db.String(200))
    # 职业
    profession = db.Column(db.String(200))
    # 单位性质
    status = db.Column(db.String(100))
    # 工作年限
    employment_year = db.Column(db.SmallInteger)
    # 工作收入
    income = db.Column(db.Float)


class Estate(db.Model):
    """
    房产
    """
    __tablename__ = 'estate'
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    # 地址
    address = db.Column(db.String(200))
    # 面积
    square = db.Column(db.Float)
    # 购买价格
    cost = db.Column(db.Float)
    # 贷款金额
    loan = db.Column(db.Float)
    # 贷款年限
    loan_year = db.Column(db.SmallInteger)
    # 已还款时间
    payments_year = db.Column(db.SmallInteger)
    # 状态，出租或自住
    status = db.Column(db.String(10))
    # 出租月租
    rental = db.Column(db.DECIMAL)


class Lodging(db.Model):
    """
    租房情况
    """
    __tablename__ = 'lodging'
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    # 租房地址
    address = db.Column(db.String(200))
    # 租房面积
    square = db.Column(db.Float)
    # 租金
    month_amount = db.Column(db.DECIMAL)
    # 开始租住时间
    begin_time = db.Column(db.DateTime)


class PersonRisk(db.Model):
    """
    个人风险，对应鹏远个人身份认证信息接口
    """
    __tablename__ = 'person_risk'
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    # 司法案例数量
    judicial_case = db.Column(db.SmallInteger)
    # 司法执行数量
    judicial_performed = db.Column(db.SmallInteger)
    # 司法失信数量
    judicial_blacklist = db.Column(db.SmallInteger)
    # 税务行政执法信息条数
    tax_performed = db.Column(db.SmallInteger)
    # 催欠公告信息条数
    tax_debt = db.Column(db.SmallInteger)
    # 网贷逾期信息条数
    loan_expired = db.Column(db.SmallInteger)


class BankCard(db.Model):
    """
    银行卡信息，对应鹏元开户行信息查询
    """
    __tablename__ = 'bank_card'
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    # 银行卡号
    card_num = db.Column(db.String(20))
    # 开户银行
    bank_name = db.Column(db.String(200))
    # 卡类型
    card_class = db.Column(db.String(20))
    # 卡种名称
    card_name = db.Column(db.String(20))
    # 开户行所在省
    bank_province = db.Column(db.String(20))
    # 开户行所在城市
    bank_city = db.Column(db.String(20))
    # 开户时间
    open_date = db.Column(db.DateTime)
    # 账目流水
    records = db.relationship('MoneyRecord', backref='bank')


class AirTraffic(db.Model):
    """
    航空出行
    """
    __tablename__ = 'air_traffic'
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    # 最频繁飞行月份
    most_month = db.Column(db.String(6))
    # 最频繁飞行月份占比
    most_month_percent = db.Column(db.String(6))
    # 平均折扣区间
    avg_discount_area = db.Column(db.Text)
    # 商务舱所占百分比
    business_cabin_percent = db.Column(db.String(6))
    # 公务舱所占百分比
    official_cabin_percent = db.Column(db.String(6))
    # 经济舱所占百分比，如10
    economy_cabin_percent = db.Column(db.String(6))
    # 频繁出发城市前三，以分号隔开
    from_city = db.Column(db.Text)
    # 频繁出发城市前三所占百分百
    from_city_percent = db.Column(db.Text)
    # 频繁到达城市前三
    dest_city = db.Column(db.Text)
    # 频繁到达城市前三所占百分百
    dest_city_percent = db.Column(db.Text)
    # 乘坐最多的航空公司名称，可能为空
    most_airline = db.Column(db.Text)
    # 乘坐最多的航空公司占比，可能为空
    most_airline_percent = db.Column(db.Text)
    # 国内乘机次数所占百分比
    domestic_percent = db.Column(db.String(6))
    # 国际乘机次数所占百分比
    inter_percent = db.Column(db.String(6))
    # 免费乘机次数占比
    free_percent = db.Column(db.String(6))
    # 平均票价
    avg_price = db.Column(db.Float)
    # 平均延迟时间所在区间
    avg_delay_area = db.Column(db.Text)
    # 平均提前出票时间所在区间
    avg_ticket_day_area = db.Column(db.Text)
    # 最后乘机日期所在区间
    last_flight_date_area = db.Column(db.Text)
    # 飞行指数级别
    fly_count_level = db.Column(db.String(10))
    # 飞行次数名称
    fly_count_name = db.Column(db.String(10))
    # 飞行次数所在区间，可能为空
    fly_count_area = db.Column(db.String(10))
    # 飞行指数等级区间
    grade_desc = db.Column(db.String(10))
    # 舱级描述信息
    cabin_desc = db.Column(db.String(20))
    # 飞行指数
    fly_score = db.Column(db.String(20))
    # 舱级评分
    cabin_score = db.Column(db.String(6))


class MoneyRecord(db.Model):
    """
    银行流水
    """
    __tablename__ = 'money_record'
    id = db.Column(db.Integer, primary_key=True)
    bank_id = db.Column(db.Integer, db.ForeignKey('bank_card.id'))
    # 交易时间
    transaction_time = db.Column(db.DateTime)
    # 金额
    transaction_money = db.Column(db.DECIMAL)
    # 类型 收入或支出
    transaction_type = db.Column(db.String(10))


class BankReport(db.Model):
    """
    银行卡综合分析，对应银联数据
    """
    __tablename__ = 'bank_report'
    id = db.Column(db.Integer, primary_key=True)
    bank_id = db.Column(db.Integer, db.ForeignKey('bank_card.id'))


class Investment(db.Model):
    """
    金融投资情况
    """
    __tablename__ = 'investment'
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    # 投资类型 股票、理财和储蓄等
    type = db.Column(db.String(10))
    # 投资金额
    amount = db.Column(db.DECIMAL)


class Loan(db.Model):
    """
    贷款情况
    """
    __tablename__ = 'loan'
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    # 贷款对象
    loan_name = db.Column(db.String(100))
    # 贷款金额
    loan_amount = db.Column(db.DECIMAL)
    # 贷款时间
    loan_time = db.Column(db.DateTime)
    # 贷款状态（是否还清）
    loan_status = db.Column(db.String(10))
    # 剩余余额
    loan_left = db.Column(db.DECIMAL)


class LoanGuarantee(db.Model):
    """
    担保情况
    """
    __tablename__ = 'loan_guarantee'
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    # 担保金额
    guarantee_amount = db.Column(db.DECIMAL)
    # 担保期限(单位年)
    guarantee_period = db.Column(db.Float)
    # 开始担保时间
    guarantee_time = db.Column(db.DateTime)
    # 担保原因
    guarantee_reason = db.Column(db.Text)


class Vehicle(db.Model):
    """
    机动车，对应鹏元车辆信息,没有完全对应，有些是否需要再综合下
    """
    __tablename__ = 'vehicle'
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    # 车牌号
    license = db.Column(db.String(20))
    # 登记所有人
    owner_name = db.Column(db.String(20))
    # 登记人证件号
    owner_identity = db.Column(db.String(18))
    # 品牌
    brand = db.Column(db.String(100))
    # 厂家
    manufacturer = db.Column(db.String(100))
    # 购买价格
    buy_price = db.Column(db.DECIMAL)
    # 购买年份
    buy_year = db.Column(db.String(4))


class Company(db.Model):
    """
    经营企业
    """
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    # 名称
    name = db.Column(db.String(200))
    # 企业法人
    legal_representative = db.Column(db.String(10))
    # 地址
    address = db.Column(db.String(200))
    # 工商注册号
    register_number = db.Column(db.String(200))
    # 成立日期
    open_date = db.Column(db.Date)
    # 员工数量
    employee_count = db.Column(db.SmallInteger)


class Consumption(db.Model):
    """
    消费情况
    """
    __tablename__ = 'consumption'
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
