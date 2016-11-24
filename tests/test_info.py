# -*- coding: utf-8 -*-


from unittest import TestCase
from app import create_app, db
from app.info import *
import json


def convert_obj(obj, *complex_name):
    convert = {}
    for name, value in obj.__dict__.items():
        if value is None:
            continue
        if name[0] is not '_' and name is not 'person_id'\
                and name is not 'bank_id' and name is not 'id':
            convert[name] = value
    for item in complex_name:
        complex_classes = getattr(obj, item)
        complex_list = []
        for temp in complex_classes:
            if item is 'bank_card':
                complex_list.append(convert_obj(temp, 'records'))
            else:
                complex_list.append(convert_obj(temp))
        convert[item] = complex_list
    return convert


class TestInfo(TestCase):
    p = Person(name='张三', identity='123456789012345678')
    f = Family(name='张小明', relation='儿子', person=p)
    phone = Telephone(number='123456789', person=p)
    unit = Unit(person=p)
    estate = Estate(person=p)
    lodging = Lodging(person=p)
    person_risk = PersonRisk(person=p)
    bank_card = BankCard(person=p)
    money_record = MoneyRecord(bank=bank_card)
    investment = Investment(person=p)
    loan = Loan(person=p)
    loan_guarantee = LoanGuarantee(person=p)
    vehicle = Vehicle(person=p)
    company = Company(person=p)

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        db.session.add(self.p)
        db.session.commit()

    def tearDown(self):
        db.session.delete(self.p)
        db.session.commit()

    def test_query(self):
        p = Person.query.filter_by(name='张三').first()
        d = convert_obj(p, 'family', 'phone', 'unit', 'estate', 'lodging',
                        'person_risk', 'bank_card', 'investment', 'loan',
                        'loan_guarantee', 'vehicle', 'company')
        print(json.dumps(d, indent=2, ensure_ascii=False,sort_keys=True))
